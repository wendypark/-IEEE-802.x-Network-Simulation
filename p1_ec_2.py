import random
import math
#import scipy.stats 
#import pareto_distribution

#global variables 
MAXBUFFER = float('inf')	# max size of buffer for exp 1
LENGTH = 0 					# number of packets in queue + server
TIME = 0					# current time
SERVICE_RATE = 1			# u
PACKETS_DROPPED = 0 		# number of packets dropped
MEAN_QUEUE_LENGTH = 0		# length of packet * time 
SERVER_BUSY_TIME = 0		# server occupied

# SECTION: 3.1 
# Event Object 
class Event(object):
	def __init__(self, event_time=None, event_type=None):
		self.e_time = event_time
		self.e_type = event_type
		self.next = None

	def setEventType(self, ev_type):
		self.e_type = ev_type

	def setEventTime(self, ev_time):
		self.e_time = ev_time

	def curEventType(self):
		return self.e_type

	def eventTime(self):
		return self.e_time


# SECTION: 3.1
# GEL Object
class GlobalEventList(object):
	def __init__(self, event_list=None):
		self.head = None

	def insertEvent(self, incoming_event):
		# empty list
		if self.head is None:
			incoming_event.next = self.head 	# points to nothing
			self.head = incoming_event			# becomes head

		# at least one element in there
		elif self.head.e_time >= incoming_event.e_time:
			incoming_event.next = self.head 	# points to previous head
			self.head = incoming_event			# becomes head

		#GLE full
		else:
			cur_event = self.head
			while cur_event.next is not None and cur_event.next.e_time < incoming_event.e_time:
				cur_event = cur_event.next

			incoming_event.next = cur_event.next
			cur_event.next = incoming_event
	
	#packet ready for transmission 
	def removeFirstEvent(self):
		self.head = self.head.next

	def firstEvent(self):
		return self.head



# SECTION: 3.1
# Buffer Object
class Buffer(object):
	# NOTE: using list as a queue
	# top of the queue is the last element in list
	def __init__(self, max_buffer):
		self.max_b = max_buffer
		self.buff = []

	def insertPacket(self, incoming_packet):
		# insert at beginning of list or end of queue
		self.buff.insert(0, incoming_packet)

	def removePacket(self):
		if len(self.buff) != 0:
			# remove last element in list or first in queue
			self.buff.pop() 
		else:
			print "Buffer is empty."

	def curBufferSize(self):
		return len(self.buff)

	def topPacket(self):
		return self.buff[len(self.buff)-1]

	def curPacketServiceTime(self):
		return self.topPacket().getServiceTime()



# SECTION: 3.1
# Packet Object
class Packet(object):
	def __init__(self, service_time):
		self.service_t = service_time
	
	def getServiceTime(self):
		return self.service_t



# SECTION: 3.3
# Arrival Event 
def processArrivalEvent(buff, gel):
	global TIME 
	global LENGTH
	global MEAN_QUEUE_LENGTH
	global SERVER_BUSY_TIME
	global PACKETS_DROPPED

	# time of the "width" of queue
	time_difference = gel.firstEvent().eventTime() - TIME
	TIME += time_difference

	MEAN_QUEUE_LENGTH += buff.curBufferSize() * time_difference
	
	# SECTION: 3.8 EC
	# Pareto Distribution for arrival rate 
	next_arrival_time = TIME + random.paretovariate(ARRIVAL_RATE)
	new_packet = Packet(negativeExponenetiallyDistributedTime(SERVICE_RATE))
	
	new_arrival_event = Event()
	new_arrival_event.setEventType(1)
	new_arrival_event.setEventTime(next_arrival_time)

	gel.insertEvent(new_arrival_event)

	#Server is free
	if LENGTH == 0:
		serv_time = new_packet.getServiceTime()
		departure_event_time = TIME + serv_time
		
		departure_event = Event()
		departure_event.setEventType(2)
		departure_event.setEventTime(departure_event_time)

		gel.insertEvent(departure_event)

		LENGTH = 1

	#Server is busy
	else:
		# buffer not full
		if LENGTH - 1 < MAXBUFFER:
			buff.insertPacket(new_packet)
			LENGTH = buff.curBufferSize() + 1

		# buffer is full
		else:
			PACKETS_DROPPED += 1

		SERVER_BUSY_TIME += time_difference # at a particular queue




# SECTION: 3.4
# Departure Event 
def processDepartureEvent(buff, gel):
	global TIME 
	global LENGTH
	global MEAN_QUEUE_LENGTH
	global SERVER_BUSY_TIME

	# time of the "width" of queue
	time_difference = gel.firstEvent().eventTime() - TIME 
	TIME += time_difference

	MEAN_QUEUE_LENGTH += buff.curBufferSize() * time_difference
	
	SERVER_BUSY_TIME += time_difference # at a particular queue

	LENGTH -= 1

	#system not empty
	if LENGTH > 0:

		packet_transmit_time = buff.curPacketServiceTime()
		buff.removePacket()

		departure_event_time = TIME + packet_transmit_time
		departure_event = Event()
		departure_event.setEventType(2)
		departure_event.setEventTime(departure_event_time)

		gel.insertEvent(departure_event)



# SECTION: 3.6
# Time intervals in negative exponential distribution 
def negativeExponenetiallyDistributedTime(rate):
	u = random.random()
	return ((-1/rate)*math.log(1-u))

# SECTION: 3.8 EC
# Pareto Distribution 
#def pareto_distribution(rate):
#	u = random.random()
#	return (1/(1-u)**(1/rate))
	

def calculate_stats(exp, MAXBUFFER, ARRIVAL_RATE):
	
	# Event type
	# 1 : arrival
	# 2: departure 
	first_arrival_event = 1

	event = Event()
	gel = GlobalEventList()
	event.setEventType(first_arrival_event)

	# SECTION: 3.8 EC
	# Pareto Distribution for arrival rate 
	event.setEventTime(TIME + random.paretovariate(ARRIVAL_RATE))

	# inserting our first event
	gel.insertEvent(event)

	buff = Buffer(MAXBUFFER)

	for i in range(0, 100000):
		# arrival
		if gel.firstEvent().curEventType() == 1: 
			processArrivalEvent(buff, gel)
			
		# departure
		elif gel.firstEvent().curEventType() == 2:
			processDepartureEvent(buff, gel)

		# packet transmitted
		gel.removeFirstEvent()

	#STATS
	print ("Buffersize: %s" %str(MAXBUFFER))
	print ("Experiment %d, Arrival Rate %.2f" % (exp, ARRIVAL_RATE))
	print ("Mean Queue-Length = %f" % (MEAN_QUEUE_LENGTH/TIME))
	print ("Server Utilization = %f" % (SERVER_BUSY_TIME/TIME))
	print ("Number of Packets Dropped = %f \n \n" % PACKETS_DROPPED)


# SECTION: 3.1/3.2
if __name__ == '__main__':

	# Experiment 1
	ARR_RATE = [.1, .25, .4, .55, .65, .8, .9]

	for x in ARR_RATE:

		#declare global to avoid scoping issues 
		global ARRIVAL_RATE
		ARRIVAL_RATE = x

		calculate_stats(exp=1, MAXBUFFER=float('inf'), ARRIVAL_RATE=x)

		#reset global vairables 
		MAXBUFFER = float('inf')	# max size of buffer
		LENGTH = 0 					# number of packets in queue + server
		TIME = 0					# current time
		SERVICE_RATE = 1			# u
		PACKETS_DROPPED = 0 		# number of packets dropped
		MEAN_QUEUE_LENGTH = 0		# length of packet * time 
		SERVER_BUSY_TIME = 0		# server busy time


	# Experiment 3
	ARR_RATE_2 = [.2, .4, .6, .8, .9]

	for x in ARR_RATE_2:

		#declare global to avoid scoping issues 
		global ARRIVAL_RATE
		ARRIVAL_RATE = x

		MAXBUFFER = [1, 20, 50]
		for y in MAXBUFFER:

			#declare global to avoid scoping issues 
			global MAXBUFFER
			calculate_stats(exp=3, MAXBUFFER=y, ARRIVAL_RATE=x)

			#reset global vairables 
			LENGTH = 0 					# number of packets in queue + server 
			TIME = 0					# current time
			SERVICE_RATE = 1			# u
			PACKETS_DROPPED = 0 		# number of packets dropped
			MEAN_QUEUE_LENGTH = 0		# length of packet * time 
			SERVER_BUSY_TIME = 0		# server busy time
