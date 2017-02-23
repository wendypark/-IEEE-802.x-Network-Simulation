from Queue import *
import random
import math


# maximum num of packets that could be in buffer
MAXBUFFER =  100
LENGTH = 0
TIME = 0
BUFFER = Queue(MAXBUFFER)


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

	# def nextEvent(self,):

	# def previousEvent(self,):



# SECTION: 3.1
# maintain all the events sorted in increasing order of time
class GlobalEventList(object):
	def __init__(self, eventList=None):
		if eventList is None:
			self.lst = []

	def insertEvent(self, incoming_event):
		self.lst.append(incoming_event)
		# print self.lst[0]
		# sort after appending new event
		self.lst.sort(key=lambda x: x.e_time)

	def removeFirstEvent(self):
		self.lst.pop(0)



# SECTION: 3.6
def negativeExponenetiallyDistributedTime(rate):
	u = random.random()
	return ((-1/rate)*math.log(1-u))



# SECTION: 3.1/3.2
if __name__ == '__main__':
	first_arrival_event = 1

	event = Event()
	gel = GlobalEventList()

	event.setEventType(first_arrival_event)

	# 0.1 is the initial arrival rate
	event.setEventTime(TIME + negativeExponenetiallyDistributedTime(0.1))

	# inserting our first event
	gel.insertEvent(event)



	for i in range(0,100000):
		# arrival
		if gel.curEventType() == 1:


		# departure
		else:
