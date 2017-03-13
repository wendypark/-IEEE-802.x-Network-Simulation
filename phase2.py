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

TOTAL_SUCCESSFULL_BYTES = 0



class Event(object):
	def __init__(self):
		self.e_time = None
		self.e_type = None
		self.e_secondary_type = None
		self.e_sending_host = None
		self.e_receiving_host = None
		self.e_size = None
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

	def setEventSize(self, ev_size):
		self.e_size = ev_size

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
	
	# packet ready for transmission 
	def removeFirstEvent(self):
		self.head = self.head.next

	def firstEvent(self):
		return self.head


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
		self.backoff_cnt = 0


def processArrivalEvent(buff, gel):
	if gel.firstEvent().e_secondary_type == "sensing: data packet arriving":		# from channelSensingEvent
		LINK_BUSY = false
		new_ack_depart_event = Event()
		new_ack_depart_event.setEventType(2) 										# departing event
		new_ack_depart_event.setSecondaryEventType("sensing: ack packet departing") # going to sending host 
		new_ack_depart_event.setEventTime(TIME + SIFS) 								# when you get to this time in gel, it means ack needs to be sent
		new_ack_depart_event.setEventSendingHost(gel.firstEvent().e_sending_host)
		new_ack_depart_event.setEventReceivingHost(gel.firstEvent().e_receiving_host)

	elif gel.firstEvent().e_secondary_type === "sensing: ack packet arriving"
		LINK_BUSY = false

		TOTAL_SUCCESSFULL_BYTES += gel.firstEvent().e_size 	# original size of packet
		TOTAL_SUCCESSFULL_BYTES += 64 						# ack size

		# host has been notified that data has been successfully transmitted
		hosts[gel.firstEvent().e_host].host_inf_queue.removePacket()	# remove successfully transmitted packet from host's queue

		# next departure event for next packet in host's queue
		next_packet = hosts[gel.firstEvent().e_host].host_inf_queue.topPacket()
		
		next_event = Event()
		new_ack_depart_event.setEventType(2) 											# departing from sending host
		new_ack_depart_event.setSecondaryEventType("sensing: sensing packet departing")	
		new_ack_depart_event.setEventTime(TIME + new_packet.service_t) 					# new packet's service time					
		new_ack_depart_event.setEventSendingHost(gel.firstEvent().e_sending_host)		
		new_ack_depart_event.setEventReceivingHost(gel.firstEvent().e_receiving_host)	# send to same host again

		gel.removeFirstEvent()


def channelSensingEvent(gel):
	if not LINK_BUSY:
		hosts[gel.firstEvent().e_host].backoff_cnt -= 1	# decrement current host's backoff count
														# only decrement here because backoff needs to remain frozen otherwise
		
		# if current host backoff is completed
		if hosts[gel.firstEvent().e_host].backoff_cnt == 0:
			# CORRECT WAY TO UPDATE TIME?
			time_difference = gel.firstEvent().eventTime() - TIME 
			TIME += time_difference

			packet_to_be_transmitted = hosts[gel.firstEvent().e_host].host_inf_queue.topPacket() 	# need to create packet somewhere though

			new_data_arrival_event = Event()
			new_data_arrival_event.setEventType(1) 													# arrival event
			new_data_arrival_event.setSecondaryEventType("sensing: data packet arriving") 			# going to sending host 
			new_data_arrival_event.setEventTime(TIME + DIFS>)	# TIME FORMULA?
			new_data_arrival_event.setEventSendingHost(gel.firstEvent().e_receiving_host) 			# receiving host becomes sending host
			new_data_arrival_event.setEventReceivingHost(gel.firstEvent().e_sending_host)			# need to use this to make departure destination later
			gel.insertEvent(new_data_arrival_event)

			# SIFS timer aka receiving host waiting
			SIFS_timer_event = Event()
			SIFS_timer_event.setEventType(-1)
			SIFS_timer_event.setSecondaryEventType("sensing: SIFS timeout")
			SIFS_timer_event.setEventTime(TIME + SIFS + <something????>)	# TIME FORMULA?
			SIFS_timer_event.setEventSendingHost(gel.firstEvent().e_sending_host)					# waiting for the sending host
			SIFS_timer_event.setEventReceivingHost(gel.firstEvent().e_receiving_host)
			gel.insertEvent(SIFS_timer_event)
	
	# link is busy
	else:
		# FOLLOWING THE GIVEN ALGO, IT DOESN'T MAKE SENSE TO CREATE A RANDOM BACKOFF EVERY TIME CHANNEL IS BUSY...THOUGHTS?
		busy_channel_event = Event()
		busy_channel_event.setEventType(3)													# try channelSensingEvent later
		busy_channel_event.setSecondaryEventType("sensing: try sending, but channel busy") 
		rand_backoff = int(round(random.randint(0,1) * T))									# randomly generated backoff
		busy_channel_event.setEventTime(rand_backoff)
		busy_channel_event.setEventSendingHost(gel.firstEvent().e_sending_host)
		busy_channel_event.setEventReceivingHost(gel.firstEvent().e_receiving_host)
		gel.insertEvent(busy_channel_event)


def variousTimers(gel):


if __name__ == '__main__':

	gel = GlobalEventList()

	all_hosts = []
	for i in range (0, num_host):
		all_host[i] = Host()
		new_event = Event()
		new_event.setEventType(3) 			# channel-sensing event. continuing numbering protocol from Phase 1
		new_event.setSecondaryEventType(0) 	# not important at initialization
		new_event.setEventTime(TIME) 		# initialized to 0
		new_event.setEventSendingHost(i)	
		dest_host = random.randint(0,NUM_HOST)
		# make sure sending host doesn't send packet to itself
		while i == dest_host:
			dest_host = random.randint(0,NUM_HOST)
		new_host.setEventReceivingHost(dest_host)	# random destination host


	for i in range(0, NUM_OF_FRAMES):
		# if statement here because not sure if we need to incorporate other events from Phase 1



		if gel.firstEvent().curEventType() == 3:
			channelSensingEvent(gel)

		# SIFS timer runs out
		if gel.firstEvent().curEventType() == -1:	
			variousTimers(gel)


		gel.removeFirstEvent()

