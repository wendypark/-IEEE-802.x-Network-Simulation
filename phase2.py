import random
import math

SIFS = 0.05
DFS = 0.1
SENSE = 0.01
NUM_OF_FRAMES = 100000
TIME = 0
LINK_BUSY = false
LAMBDA = 10 
NUM_HOST = 10
T_VALUE =  1



class Event(object):
	def __init__(self, event_time=None, event_type=None, event_sending_host=None, event_receiving_host=None, event_secondary_type=None):
		self.e_time = event_time
		self.e_type = event_type
		self.e_secondary_type = event_secondary_type
		self.e_sending_host = event_sending_host
		self.e_receiving_host = event_receiving_host
		self.next = None

	def setEventType(self, ev_type):
		self.e_type = ev_type

	def setSecondaryEventType(self, ev_sec_type):
		self.e_secondary_type = ev_sec_type

	def setEventTime(self, ev_time):
		self.e_time = ev_time

	def setEventSendingHost(self, ev_send_host):
		self.e_sending_host = ev_send_host

	def setEventReceivingHost(self, ev_receive_host):
		self.e_receiving_host = ev_receive_host

	def curEventType(self):
		return self.e_type

	def eventTime(self):
		return self.e_time


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


# class Link(object):
# 	def __init__():
# 		self.link_busy = false 

# 	def checkStatus(self):
# 		return self.link_busy


class Packet(object):
	def __init__(self, service_time):
		self.service_t = service_time
	
	def getServiceTime(self):
		return self.service_t


class Host(object):
	def __init__(self):
		self.host_inf_queue = Buffer(float('inf'))
		self.dropped_frames = 0
		self.transmittion_time = 0


def processArrivalEvent(buff, gel, secondaryEventType):
	if secondaryEventType == "sensing: data packet arriving":
		new_ack_depart_event = Event()
		new_ack_depart_event.setEventType(2) # departing event
		new_ack_depart_event.setSecondaryEventType("sensing: ack packet departing") # going to sending host 
		new_ack_depart_event.setEventTime(TIME + SIFS) # when you get to this time in gel, it means ack needs to be sent
		new_ack_depart_event.setEventSendingHost(gel.firstEvent().e_receiving_host)
		new_ack_depart_event.setEventReceivingHost(gel.firstEvent().e_sending_host)


def channelSensingEvent(gel):
	
	if not LINK_BUSY:
		hosts[gel.firstEvent().e_host].backoff_cnt -= 1 # decrement current host's backoff count
		
		# if current host backoff is completed
		if hosts[gel.firstEvent().e_host].backoff_cnt == 0:
			### need to update global time here...somehow ###
			packet_to_be_transmitted = hosts[gel.firstEvent().e_host].host_inf_queue.topPacket() # need to create packet somewhere though

			new_data_arrival_event = Event()
			new_data_arrival_event.setEventType(1) # arriving event
			new_data_arrival_event.setSecondaryEventType("sensing: data packet departing") # going to sending host 
			new_data_arrival_event.setEventTime(TIME + <((cur_packet.size * 8)/(11*10^6)) + DIFS>) # when you get to this time in gel, it means ack needs to be sent
			new_data_arrival_event.setEventSendingHost(gel.firstEvent().e_sending_host) # receving host becomes sending host
			new_data_arrival_event.setEventReceivingHost(gel.firstEvent().e_receiving_host)


			### need to check logic for departing and arriving events (ark and data) ###

 			
 			# SIFS event goes here as well



if __name__ == '__main__':

	gel = GlobalEventList()

	all_hosts = []
	for i in range (0, num_host):
		all_host[i] = Host()
		new_event = Event()
		new_event.setEventType(3) # channel-sensing event. continuing numbering protocol from Phase 1
		new_event.setSecondaryEventType(0) # not important at initialization
		new_event.setEventTime(TIME) # just start at time zero
		new_event.setEventSendingHost(i)
		dest_host = random.randint(0,NUM_HOST)
		# make sure sending host doesn't send packet to itself
		while i == dest_host:
			dest_host = random.randint(0,NUM_HOST)
		new_host.setEventReceivingHost(dest_host)


	for i in range(0, NUM_OF_FRAMES):
		# if statement here because not sure if we need to incorporate other events from Phase 1

		if gel.firstEvent().curEventType() == 3:
			channelSensingEvent(gel)






