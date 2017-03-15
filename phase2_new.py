import math
import random

TIME = 0		# Global Time
DIFS = 0.1		# Sending host wait time
SIFS = 0.05		# Receiving host wait time
BUSY = False	# Link status



class Event(object):

	def __init__(self,event_type,sending_host,receiving_host):
		self.type = type_event
		self.sending_host = sending_host
		self.receiving_host = receiving_host


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

    def __init__(self,idx,):
        self.host_queue = Buffer(float('inf'))
        self.idx = idx
        self.transmission_time = 0
        self.backoff_counter = 0
        self.trans_delay = 0
        self.queue_delay = 0


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


def processArrivalEvent(hosts, gel, cur_ev):
	global TIME
	global BACKOFF_HOSTS

	# Generate next arrival event similar to Phase 1
	next_arrival_event = Event('1', cur_ev.sending_host, cur_event.receiving_host)
	gel.insertEvent(first_arrival_event)

	# Generate new packet
	new_packet = Packet(cur_event.sending_host, cur_ev.receiving_host, negativeExponenetiallyDistributedSize())
	HOSTS[cur_event.sending_host].host_queue.insertPacket(new_packet)

	# check if recently inserted packet is only packet in host's queue
	queue_size = HOSTS[cur_event.sending_host].host_queue.curBufferSize()
	if queue_size == 1:
		if not BUSY:
			# transmit if not busy
			transmission_event = Event('1', cur_event.sending_host, cur_event.receiving_host, DIFS + TIME)	# transmit, sending host idx, destination host index
		else:
			# backoff
			if cur_event.sending_host not in BACKOFF_HOSTS
				rand_backoff = int(round(random.randint(0, 1) * T))
				HOSTS[cur_event.sending_host].backoff_counter = rand_backoff
				BACKOFF_HOSTS.append(cur_event.sending_host)
			else:
				# do nothing since host is still waiting


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

    	# check link every iteration
    	if BUSY == False:
    		decrementBackoffs(BACKOFF_HOSTS)

    	if ev.type == '1':
    		processArrivalEvent(gel, ev)

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