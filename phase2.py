SIFS = 0.05
DFS = 0.1
SENSE = 0.01 

class Link(object):
	def __init__():
		self.link_busy = false 

	def checkStatus(self):
		return self.link_busy


class Frame(object):
	def __init__(self, transmitted_time):
		self.time_transmitted = transmitted_time
		self.ack_status = false


class Host(object):
	def __init__(self):
		self.outstanding_frames = Buffer(inf)
		self.sent_timer  = 0

	def setSentTimer(self,sent_time):
		self.sent_timer = sent_time


