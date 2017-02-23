# from Queue import *
import random
import math


MAXBUFFER =  100
LENGTH = 0
TIME = 0



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

		# sort after appending new event
		self.lst.sort(key=lambda x: x.e_time)

	def removeFirstEvent(self):
		self.lst.pop(0)



# SECTION: 3.1
class Buffer(object):
	def __init__(self, max_buffer=None):
		self.max_b = max_buffer
		buff = Queue(max_buffer)

	def insertPacket(self, incoming_packet):
		if buff.size() <= self.max_b:
			buff.enqueue(incoming_packet)
		else:
			print "buffer is full. packet dropped."

	def removePacket(self):
		if buff.size() != 0:
			buff.dequeue()
		else:
			print "buffer is empty"



# SECTION: 3.3
def processArrivalEvent():



# SECTION: 3.4
def processDepartureEvent():



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

	for i in range(0,100000):
		# arrival
		if gel.curEventType() == 1:


		# departure
		else:

