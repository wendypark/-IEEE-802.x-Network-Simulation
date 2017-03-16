import math
import random

TIME = 0		# Global Time
DIFS = 0.1		# Sending host wait time
SIFS = 0.05		# Receiving host wait time
BUSY = False	# Link status
HOSTS = []
BACKOFF_HOSTS = []
CHANNEL_CAP = 11*(10**6)        # channel transmission capacity is 11Mbps
NUM_HOST = 10


class Event(object):

	def __init__(self,event_type,sending_host,receiving_host,time):
		self.type = event_type
		self.sending_host = sending_host
		self.receiving_host = receiving_host
		self.time = time

	# def setIsAck(self,)


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
            print 'Buffer is empty.'

    def curBufferSize(self):
        return len(self.buff)

    def topPacket(self):
        return self.buff[len(self.buff) - 1]

    def curPacketServiceTime(self):
        return self.topPacket().getServiceTime()


class Host(object):

    def __init__(self,idx):
        self.host_queue = Buffer(float('inf'))
        self.idx = idx
        self.transmission_time = 0
        self.backoff_counter = 0
        self.trans_delay = 0
        self.queue_delay = 0


class Packet(object):

    def __init__(self, service_time, p_size, ack=False):
        self.service_t = service_time
        self.packet_size = p_size
        self.ack = ack

    def getServiceTime(self):
        return self.service_t

    def getPacketSize(self):
        return self.packet_size


def negativeExponenetiallyDistributedSize():
    u = random.randint(0, 1544)
    return u


def decrementBackoffs(BACKOFF_HOSTS):
	global TIME

	# sensing every 0.01
	TIME += 0.01
	# need to decrement all hosts backoff counter since link is free
	for i in BACKOFF_HOSTS:
		HOSTS[i].backoff_counter -= 1


def successful_send_receive(gel,cur_event):
	# remove packet that was sent successfully
	HOSTS[cur_event.sending_host].host_queue.removePacket()

	# make new ready event for next packet in queue
	queue_size = HOSTS[cur_event.sending_host].host_queue.curBufferSize()
	if queue_size != 0:
		ready_event = Event(2, cur_event.sending_host, cur_event.receiving_host, DIFS + TIME)	# ready, sending host idx, destination host index
		gel.insertEvent(ready_event)
	else:
		print "no more packets in host's queue"


def processArrivalEvent(gel, cur_ev):
	global TIME
	global BACKOFF_HOSTS

	# generate next arrival event similar to Phase 1
	# create service time of next arrival event

	ran_time = negativeExponenetiallyDistributedTime(ARRIVAL_RATE) + TIME
	next_arrival_event = Event(1, cur_ev.sending_host, cur_event.receiving_host, ran_time)
	gel.insertEvent(first_arrival_event)

	# generate new packet
	new_packet = Packet(cur_event.sending_host, cur_ev.receiving_host, negativeExponenetiallyDistributedSize())
	HOSTS[cur_event.sending_host].host_queue.insertPacket(new_packet)

	# check if recently inserted packet is only packet in host's queue
	queue_size = HOSTS[cur_event.sending_host].host_queue.curBufferSize()
	if queue_size == 1:
		ready_event = Event(2, cur_event.sending_host, cur_event.receiving_host, DIFS + TIME)	# ready, sending host idx, destination host index
		gel.insertEvent(ready_event)


def processReadyEvent(gel,cur_event):
	global TIME

	if not BUSY:
		# create departure event
		BUSY = True
		packet_size = HOSTS[cur_event.sending_host].host_queue.topPacket().getPacketSize()
		new_departure_event = Event(2, cur_event.sending_host, cur_event.receiving_host, TIME + ((packet_size*8)/CHANNEL_CAP))
		gel.insertEvent(new_departure_event)

		# check whether packet we just sent was an acknowledgement packet
		# cur_packet = HOSTS[cur_event.sending_host].host_queue.topPacket()
		# if cur_packet.ack == False:
		# 	cur_packet.ack_needed = True
		# else:
		successful_send_receive(gel, cur_event)

		# successfully send
		TOTAL_SUCCESSFULL_BYTES += packet_size
		HOSTS[cur_event.sending_host].trans_delay += packet_size
		HOSTS[cur_event.sending_host].queue_delay += HOSTS[cur_event.sending_host].host_queue.topPacket().getServiceTime()

	else:
		if cur_event.sending_host not in BACKOFF_HOSTS:
			rand_backoff = int(round(random.randint(0, 1) * T))
			HOSTS[cur_event.sending_host].backoff_counter = rand_backoff
			BACKOFF_HOSTS.append(cur_event.sending_host)



if __name__ == '__main__':
	
	gel = GlobalEventList()

	# create hosts
	for i in range(0, NUM_HOST):
		HOSTS.append(Host(i))

        dest_host = random.randint(0, NUM_HOST)  
        while i == dest_host:
            dest_host = random.randint(0, NUM_HOST)

        first_arrival_event = Event('1', i, dest_host, TIME)	# arrival, sending host idx, destination host index, time
        gel.insertEvent(first_arrival_event)

    # start
	for i in range(0, 100000):
		ev = gel.firstEvent()
		print ev

		# check link every iteration
		if BUSY == False:
			decrementBackoffs(BACKOFF_HOSTS)

		if ev.type == 1:
			processArrivalEvent(gel, ev)

		elif ev.type == 2:
			processReadyEvent(gel, ev)

		gel.removeFirstEvent()






# processArrivalEvent
# 	- similar to what we had before

# processReadyEvent
# 	# process all the packets that needs to be transmitted
# 	- if not busy:
# 		we crease a response event. this means that we have successfully transmit
# 		make channel busy
# 		if this is not an ack packet:
# 			indicate that the host sending host is waiting for an ack packet
# 		else:
# 			remove packet
# 			indicate that host is not waiting for ack
# 			generate next packet transmission
# 	- else:
# 		backoff
#	


# processResponseEvent
# 	# destination host create the acknowledgement packet