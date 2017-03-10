import random
import math

# CSMA/CA Protocol = 802.11 WLAN
# when host transmits, all other hosts recongize 
# all hosts transmit on one error-free channel, if no collision all transmissions will be successful 

#global variables 
N = 10 						# number of identical hosts
BUFFER = float('inf')		# size of each buffer/host 
ACK_FRAME = 64				# fixed size for ack frame 
CHANNEL_SIZE = 11*(10**6)   # channel size capacity

class Channel(object):
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
	

class Host(object):

class Frame(object):




def random_backoff_value(x):
	#host choss

def calculate_stats():


	transmission_time = (r*8)/CHANNEL_SIZE #time to transmit data_frame

	throughput = TOTAL_BYTES/TOTAL_TIME
	avg_network_delay = TOTAL_DELAY / throughput
	

# Main 
if __name__ == '__main__':

	# Experiment 1
	ARR_RATE = [.01, .05, 0.1, 0.3, 0.6, 0.8, 0.9]

	for x in ARR_RATE:

		#declare global to avoid scoping issues 
		global ARRIVAL_RATE
		ARRIVAL_RATE = x

		calculate_stats(exp=1, MAXBUFFER=float('inf'), ARRIVAL_RATE=x)

		#reset global vairables 
		N = 10 							# number of identical hosts
		BUFFER = float('inf')			# size of each buffer/host 
		ACK_FRAME = 64					# fixed size for ack frame 
		CHANNEL_SIZE = 11*(10**6)   	# channel size capacity
		r = random.random(1, 1545)  	# data_frame length 
		TOTAL_BYTES = 0					# total # of bytes successfully transmitted 
		TOTAL_TIME = 0 					# whole simulation time 
		TOTAL_DELAY = 0 				# total delay = queuing delay + transmission delay 
		SIFS = .05*(10**-3)		
		DIFS = .1*(10**-3)
		SENSE_IDLE = .01*(10**-3)		#every .01 msec check that channel is busy or not 


# link-layer acknowledgment:

#pseudocode for link-layer acknowledgement:
if channel = idle:
	DIFS -= 1 until 0
	host transmit data_frame
else:
	host_counter = random_backoff_value:
	if channel = idle:
		counter -= 1
		if counter = 0:
			host transmit data_frame, then waits for ack 
			if receive_host receives frame:
				SIFS -=1 until 0
				receive_host send back ack_frame 
	else:
		counter frozen 



