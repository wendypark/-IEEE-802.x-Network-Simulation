# from Queue import *
import random
import math


MAXBUFFER = float('inf')		# max size of buffer
LENGTH = 0 			# number of packets in queue
TIME = 0			# current time
SERVICE_RATE = 1	# u
ARRIVAL_RATE = 0.1  # lambda

PACKETS_DROPPED = 0 # number of packets dropped

MEAN_QUEUE_LENGTH = 0
SERVER_BUSY_TIME = 0



# SECTION: 3.1
class Event(object):
	def __init__(self, event_time=None, event_type=None):
		self.e_time = event_time
		self.e_type = event_type

	def setEventType(self, ev_type):
		self.e_type = ev_type

	def setEventTime(self, ev_time):
		self.e_time = ev_time

	def curEventType(self):
		return self.e_type

	def getEventTime(self):
		return self.e_time

	# def nextEvent(self):

	# def previousEvent(self):



# SECTION: 3.1
# maintain all the events sorted in increasing order of time
class GlobalEventList(object):
	def __init__(self, event_list=None):
		if event_list is None:
			self.lst = []

	def insertEvent(self, incoming_event):
		self.lst.append(incoming_event)
		# print "UNSORTED"
		# for i in range(0,len(self.lst)):
		# 	print self.lst[i].getEventTime()
		# sort after appending new event
		self.lst.sort(key=lambda x: x.e_time)
		# print "SORTED"
		# for i in range(0,len(self.lst)):
		# 	print self.lst[i].getEventTime()
	
	def removeFirstEvent(self):
		self.lst.pop(0)

	def getFirstEvent(self):
		return self.lst[0]



# SECTION: 3.1
class Buffer(object):
	# NOTE: using list as a queue
	# top of the queue is the last element in list
	def __init__(self, max_buffer):
		self.max_b = max_buffer
		self.buff = []

	def insertPacket(self, incoming_packet):
		# insert at beginning of list or end of queue
		self.buff.insert(0,incoming_packet)

	def removePacket(self):
		if len(self.buff) != 0:
			buff.pop()
		else:
			print "buffer is empty"

	def curBufferSize(self):
		return len(self.buff)

	def topPacket():
		return self.buff[self.buff.size()-1]

	def curPacketServiceTime(self):
		return self.buff.topPacket().getServiceTime()



class Packet(object):
	def __init__(self, service_time):
		self.service_t = service_time
	
	def getServiceTime(self):
		return self.service_t



# SECTION: 3.3
def processArrivalEvent(buff, gel):
	global TIME 
	global LENGTH
	global MEAN_QUEUE_LENGTH
	global SERVER_BUSY_TIME
	global PACKETS_DROPPED

	TIME += gel.getFirstEvent().getEventTime()
	
	next_arrival_time = TIME + negativeExponenetiallyDistributedTime(ARRIVAL_RATE)
	new_packet = Packet(negativeExponenetiallyDistributedTime(SERVICE_RATE))
	
	new_arrival_event = Event()
	new_arrival_event.setEventType(1)
	new_arrival_event.setEventTime(TIME + negativeExponenetiallyDistributedTime(next_arrival_time))

	gel.insertEvent(new_arrival_event)

	if LENGTH == 0:
		serv_time = new_packet.getServiceTime()
		departure_event_time = TIME + serv_time
		
		departure_event = Event()
		departure_event.setEventType(2)
		departure_event.setEventTime(departure_event_time)

		gel.insertEvent(departure_event)

		LENGTH = 1
	
	else:
		# buffer not full
		if LENGTH - 1 < MAXBUFFER:
			buff.insertPacket(new_packet)
			LENGTH = buff.curBufferSize() + 1

		# full buffer
		else:
			PACKETS_DROPPED += 1
			# print "buffer is full. packet dropped."

	MEAN_QUEUE_LENGTH = buff.curBufferSize() + 1
	# SERVER_BUSY_TIME = 



# SECTION: 3.4
def processDepartureEvent(buff, gel):
	global TIME 
	global LENGTH
	global MEAN_QUEUE_LENGTH
	global SERVER_BUSY_TIME

	TIME += gel.getFirstEvent().getEventTime()

	MEAN_QUEUE_LENGTH = buff.curBufferSize() + 1
	# SERVER_BUSY_TIME = 

	LENGTH -= 1

	if LENGTH > 0:
		packet_transmit_time = buff.curPacketServiceTime()

		buff.removePacket()

		departure_event_time = TIME + packet_transmit_time
		
		departure_event = Event()
		departure_event.setEventType(2)
		departure_event.setEventTime(departure_event_time)

		gel.insertEvent(departure_event)



# SECTION: 3.6
def negativeExponenetiallyDistributedTime(rate):
	u = random.random()
	return ((-1/rate)*math.log(1-u))



# SECTION: 3.1/3.2
if __name__ == '__main__':

	first_arrival_event = 1
	initial_arrival_rate = 0.1

	event = Event()
	gel = GlobalEventList()

	event.setEventType(first_arrival_event)
	event.setEventTime(TIME + negativeExponenetiallyDistributedTime(initial_arrival_rate))

	# inserting our first event
	gel.insertEvent(event)

	buff = Buffer(MAXBUFFER)

	for i in range(0, 5000):
		# arrival
		if gel.getFirstEvent().curEventType() == 1: # first event
			processArrivalEvent(buff, gel)
		
		# departure
		elif gel.getFirstEvent().curEventType() == 2:
			processDepartureEvent(buff, gel)


	print ("Mean Queue-Length = %f" % MEAN_QUEUE_LENGTH)

