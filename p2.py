import Queue
import random 
import math
import numpy 
#Pseudo Code:

#Event object 
class Event():
	def __init__(self, event_type=None, event_time=None):
		while True:
			try:
				if (event_type is str && event_time is int):
					self.event_type = event_type
					self.event_time = event_time
					return (self.event_type, self.event_time)
			except ValueError:
				print "Event_type or Event_time is not valid"

#sec 3.3: Processing an Arrival Event 
def process_arrival_event(event_time):
	GLOBAL TIME = 0
	time = event_time

#sec 3.4: Processing a Departure Event 
def process_departure_event:
	time = event_time

#sec 3.6: Generating Time Intervals in Negative Exponential Distribution 
def neg_exp_dist(rate):
	u = numpy.random.uniform(0.0, 1.0)
	return ((-1/rate)*log(1-u))

if __name__ == '__main__':

	#initialize variables
	BUFFER = Queue()
	GEL = Queue()

	service_rate = 1

	arrival_rate_1 = [.1, .25, .4, .55, .65, .8, .9]
	arrival_rate_2 = [.2, .4, .6, .8, .9]

	MAXBUFFER_1 = math.inf
	MAXBUFFER_2 = [1, 20, 50]

	#LENGTH = 0
	#TIME = 0
	#EVENT_TIME = 0 

	#sec 3.7: Phase 1, experiment 1
	for number in arrival_rate_1:

		arrival_1 = number
		for i in range(0, 100000):
			event = Event(event_type=arrival)
			GEL.put(event)



	#sec 3.7: Phase 1, experiment 3
	for size in MAXBUFFER_2:
		MAXBUFFER_temp = size 

		for number in arrival_rate_2:
			arrival_2 = number
			for i in range(0, 100000):





for (i = 0; i < 100000; i++){ 
1. get the first event from the GEL; 
2. If the event is an arrival then process-arrival-event; 
3. Otherwise it must be a departure event and hence process-service-completion; } 
output-statistics; 

