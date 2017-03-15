import random
import math

# GLOBAL VARIABLES

SIFS = 0.05                     # receiving host wait time
DIFS = 0.1                      # sending host wait time
SENSE = 0.01                    # checks if channel is busy every .01 sec
NUM_OF_FRAMES = 100000          # iterations
TIME = 0                        # total time
LINK_BUSY = False               # checks if channel busy
ARRIVAL_RATE = 0.01             # lambda = packet arrival rate
NUM_HOST = 10                   # number of all_hosts
T = 1                           # arbitrary value for random backoff interval (0;n*T)
TOTAL_SUCCESSFULL_BYTES = 0     # total bytes transmitted successfully
CHANNEL_CAP = 11*(10**6)        # channel transmission capacity is 11Mbps


class Event(object):

    def __init__(self):
        self.e_time = None  # event time
        self.e_type = None  # event type
        self.e_secondary_type = None  # event secondary type: data or ack
        self.e_sending_host = None  # event sending host
        self.e_receiving_host = None  # event receiving host
        self.e_size = None  # event size
        self.next = None  # next event

    def setEventType(self, ev_type):
        self.e_type = ev_type

    def setSecondaryEventType(self, ev_sec_type):
        self.e_secondary_type = ev_sec_type

    def setEventTime(self, ev_time):
        self.e_time = ev_time

    def setEventSendingHost(self, ev_send_host):
        self.e_sending_host = ev_send_host

    def setEventReceivingHost(self, ev_receive_sending_host):
        self.e_receiving_host = ev_receive_sending_host

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
            print 'Buffer is empty.'

    def curBufferSize(self):
        return len(self.buff)

    def topPacket(self):
        return self.buff[len(self.buff) - 1]

    def curPacketServiceTime(self):
        return self.topPacket().getServiceTime()


class GlobalEventList(object):

    def __init__(self, event_list=None):
        self.head = None

    def insertEvent(self, incoming_event):

        # empty list

        if self.head is None:
            incoming_event.next = self.head  # points to nothing
            self.head = incoming_event  # becomes head
        elif self.head.e_time >= incoming_event.e_time:

        # at least one element in there

            incoming_event.next = self.head  # points to previous head
            self.head = incoming_event  # becomes head
        else:

        # GLE full

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

    def __init__(self, service_time, p_size):
        self.service_t = service_time
        self.packet_size = p_size

    def getServiceTime(self):
        return self.service_t

    def getPacketSize(self):
        return self.packet_size


class Host(object):

    def __init__(self):
        self.host_inf_queue = Buffer(float('inf'))
        self.dropped_frames = 0
        self.transmission_time = 0
        self.backoff_cnt = 0
        self.trans_delay = 0
        self.queue_delay = 0


def negativeExponenetiallyDistributedTime(rate):
    u = random.random()
    return -1 / rate * math.log(1 - u)


def negativeExponenetiallyDistributedSize():
    u = random.randint(0, 1544)
    return u


def processArrivalEvent(gel, all_hosts):
    global LINK_BUSY
    # arrival event of data frame

    if gel.firstEvent().e_secondary_type == 'starting arrival event of data frame':
        packet_size = negativeExponenetiallyDistributedSize()
        packet_service_time = negativeExponenetiallyDistributedTime(1)       # SOMETHING WRONG WITH THIS!!!
        
        new_packet = Packet(packet_service_time, packet_size)  # generate new data frame packet
        all_hosts[gel.firstEvent().e_sending_host].host_inf_queue.insertPacket(new_packet)

        next_arrival_time = TIME + negativeExponenetiallyDistributedTime(ARRIVAL_RATE)  # time of next data frame event
        next_arrival_event = Event()
        next_arrival_event.setEventType(1)  # schedule next arrival event, same as Phase 1 Sec 3.3 instructions
        next_arrival_event.setSecondaryEventType('starting arrival event of data frame')
        next_arrival_event.setEventTime(next_arrival_time)
        next_arrival_event.setEventSendingHost(gel.firstEvent().e_sending_host)
        next_arrival_event.setEventReceivingHost(gel.firstEvent().e_receiving_host)
        gel.insertEvent(next_arrival_event)

        # new departure
        new_data_departure_event = Event()
        new_data_departure_event.setEventType(2)
        new_data_departure_event.setSecondaryEventType('sensing: data packet departing')
        new_data_departure_event.setEventTime(TIME + new_packet.getServiceTime())
        new_data_departure_event.setEventSendingHost(gel.firstEvent().e_sending_host)
        new_data_departure_event.setEventReceivingHost(gel.firstEvent().e_receiving_host)
        gel.insertEvent(new_data_departure_event)

    elif gel.firstEvent().e_secondary_type== 'sensing: data packet arriving':
        LINK_BUSY = False

        packet_size_of_cur_event = all_hosts[gel.firstEvent().e_sending_host].host_inf_queue.topPacket().getPacketSize()
        all_hosts[gel.firstEvent().e_sending_host].trans_delay += (packet_size_of_cur_event * 8) / CHANNEL_CAP

        new_ack_depart_event = Event()
        new_ack_depart_event.setEventType(2)  # departing event
        new_ack_depart_event.setSecondaryEventType('sensing: ack packet departing')
        new_ack_depart_event.setEventTime(TIME + SIFS)  # when you get to this time in gel, it means ack needs to be sent
        new_ack_depart_event.setEventSendingHost(gel.firstEvent().e_sending_host)
        new_ack_depart_event.setEventReceivingHost(gel.firstEvent().e_receiving_host)
        gel.insertEvent(new_ack_depart_event)

    elif gel.firstEvent().e_secondary_type == 'sensing: ack packet arriving':
        print "SUCCESSFULL"
        LINK_BUSY = False

        #TOTAL_SUCCESSFULL_BYTES += gel.firstEvent().e_size  # original size of packet
        
        TOTAL_SUCCESSFULL_BYTES += all_hosts[gel.firstEvent().e_sending_host].host_inf_queue.packet_size()

        TOTAL_SUCCESSFULL_BYTES += 64  # ack size
        print 'total bytes round 1 %f' %TOTAL_SUCCESSFULL_BYTES

        # host has been notified that data has been successfully transmitted
        all_hosts[gel.firstEvent().e_sending_host].host_inf_queue.removePacket()

        # new departure event for next packet in host's queue
        next_packet = all_hosts[gel.firstEvent().e_sending_host].host_inf_queue.topPacket()

        next_event = Event()
        next_event.setEventType(2)
        next_event.setSecondaryEventType('sensing: data packet departing')
        next_event.setEventTime(TIME + next_packet.service_t)  # new packet's service time
        next_event.setEventSendingHost(gel.firstEvent().e_sending_host)
        next_event.setEventReceivingHost(gel.firstEvent().e_receiving_host)
        gel.insertEvent(next_event)


def processDepartureEvent(gel, all_hosts):
    global LINK_BUSY
    # # channel sensing event
    # # random backoff generated within here bc we need to check channel before sending
    
    packet_time_of_cur_event = all_hosts[gel.firstEvent().e_sending_host].host_inf_queue.topPacket().getServiceTime()
    all_hosts[gel.firstEvent().e_sending_host].queue_delay += packet_time_of_cur_event
    
    # departure of data
    if gel.firstEvent().e_secondary_type == 'sensing: data packet departing':

        if not LINK_BUSY & all_hosts[gel.firstEvent().e_sending_host].host_inf_queue.curBufferSize():
            packet_to_be_transmitted = all_hosts[gel.firstEvent().e_sending_host].host_inf_queue.topPacket()  # need to create packet somewhere though

            new_data_arrival_event = Event()
            new_data_arrival_event.setEventType(1)
            new_data_arrival_event.setSecondaryEventType('sensing: data packet arriving')
            new_data_arrival_event.setEventTime(TIME + DIFS + ((packet_to_be_transmitted.getPacketSize() * 8) / CHANNEL_CAP))  # THIS IS GOOD!
            new_data_arrival_event.setEventSendingHost(gel.firstEvent().e_receiving_host)
            new_data_arrival_event.setEventReceivingHost(gel.firstEvent().e_sending_host)
            gel.insertEvent(new_data_arrival_event)

            LINK_BUSY = True

            cur_packet_size = all_hosts[gel.firstEvent().e_sending_host].host_inf_queue.topPacket().getPacketSize()
            SIFS_timer_event = Event()
            SIFS_timer_event.setEventType(-1)
            SIFS_timer_event.setSecondaryEventType('sensing: SIFS timeout')
            SIFS_timer_event.setEventTime(TIME + SIFS + (64 * 8/CHANNEL_CAP) + ((cur_packet_size * 8)/CHANNEL_CAP))   # TIME FORMULA?
            SIFS_timer_event.setEventSendingHost(gel.firstEvent().e_sending_host)  # waiting for the sending host
            SIFS_timer_event.setEventReceivingHost(gel.firstEvent().e_receiving_host)
            gel.insertEvent(SIFS_timer_event)

        else:

        # channel busy. generate backoff

            busy_channel_event = Event()
            busy_channel_event.setEventType(3)  # try channelSensingEvent later
            busy_channel_event.setSecondaryEventType('sensing: try sending, but channel busy')
            rand_backoff = int(round(random.randint(0, 1) * T))  # randomly generated backoff
            busy_channel_event.setEventTime(rand_backoff)
            busy_channel_event.setEventSendingHost(gel.firstEvent().e_sending_host)
            busy_channel_event.setEventReceivingHost(gel.firstEvent().e_receiving_host)
            gel.insertEvent(busy_channel_event)

    elif gel.firstEvent().e_secondary_type == 'sensing: ack packet departing':

    # departure of ack

        if not LINK_BUSY:
            new_ack_arrival_event = Event()
            new_ack_arrival_event.setEventType(1)
            new_ack_arrival_event.setSecondaryEventType('sensing: ack packet arriving')
            new_ack_arrival_event.setEventTime(TIME + ((64 * 8) / CHANNEL_CAP))  # THIS IS GOOD!
            new_ack_arrival_event.setEventSendingHost(gel.firstEvent().e_receiving_host)
            new_ack_arrival_event.setEventReceivingHost(gel.firstEvent().e_sending_host)
            gel.insertEvent(new_ack_arrival_event)
            LINK_BUSY = True
        
        else:
            busy_channel_event = Event()
            busy_channel_event.setEventType(3)  # try channelSensingEvent later
            busy_channel_event.setSecondaryEventType('sensing: try sending, but channel busy')
            rand_backoff = int(round(random.randint(0, 1) * T))  # randomly generated backoff
            busy_channel_event.setEventTime(rand_backoff)
            busy_channel_event.setEventSendingHost(gel.firstEvent().e_receiving_host)
            busy_channel_event.setEventReceivingHost(gel.firstEvent().e_sending_host)
            gel.insertEvent(busy_channel_event)


def channelSensingEvent(gel, all_hosts):
    global TIME

    if not LINK_BUSY:
        # only decrement here because backoff needs to remain frozen otherwise
        all_hosts[gel.firstEvent().e_sending_host].backoff_cnt -= 1  # decrement current host's backoff count

    # if current host backoff is completed
    if all_hosts[gel.firstEvent().e_sending_host].backoff_cnt == 0:
        # CORRECT WAY TO UPDATE TIME?
        time_difference = gel.firstEvent().eventTime() - TIME
        TIME = gel.firstEvent().eventTime()

        packet_to_be_transmitted = all_hosts[gel.firstEvent().e_sending_host].host_inf_queue.topPacket()

        new_data_arrival_event = Event()
        new_data_arrival_event.setEventType(1)
        new_data_arrival_event.setSecondaryEventType('sensing: data packet arriving')
        new_data_arrival_event.setEventTime(TIME + DIFS + ((packet_to_be_transmitted.getPacketSize() * 8)/CHANNEL_CAP))  # TIME FORMULA?
        new_data_arrival_event.setEventSendingHost(gel.firstEvent().e_receiving_host)  # receiving host becomes sending host
        new_data_arrival_event.setEventReceivingHost(gel.firstEvent().e_sending_host)  # need to use this to make departure destination later
        gel.insertEvent(new_data_arrival_event)

            # SIFS timer aka receiving host waiting

        cur_packet_size = all_hosts[gel.firstEvent().e_sending_host].host_inf_queue.topPacket().getPacketSize()
        SIFS_timer_event = Event()
        SIFS_timer_event.setEventType(-1)
        SIFS_timer_event.setSecondaryEventType('sensing: SIFS timeout')
        SIFS_timer_event.setEventTime(TIME + SIFS + (64 * 8/CHANNEL_CAP) + ((cur_packet_size * 8)/CHANNEL_CAP))  # TIME FORMULA?
        SIFS_timer_event.setEventSendingHost(gel.firstEvent().e_sending_host)  # waiting for the sending host
        SIFS_timer_event.setEventReceivingHost(gel.firstEvent().e_receiving_host)
        gel.insertEvent(SIFS_timer_event)
    
    else:
    # link is busy
        busy_channel_event = Event()
        busy_channel_event.setEventType(3)  # try channelSensingEvent later
        busy_channel_event.setSecondaryEventType('sensing: re-sense after sense interval')
        busy_channel_event.setEventTime(TIME + SENSE)
        busy_channel_event.setEventSendingHost(gel.firstEvent().e_sending_host)
        busy_channel_event.setEventReceivingHost(gel.firstEvent().e_receiving_host)
        gel.insertEvent(busy_channel_event)


def variousTimers(gel, all_hosts):

    # send again
    new_packet = all_hosts[gel.firstEvent().e_sending_host].host_inf_queue.topPacket()
    new_data_departure_event = Event()
    new_data_departure_event.setEventType(2)
    new_data_departure_event.setSecondaryEventType('sensing: data packet departing')
    new_data_departure_event.setEventTime(TIME + new_packet.getServiceTime())
    new_data_departure_event.setEventSendingHost(gel.firstEvent().e_sending_host)
    new_data_departure_event.setEventReceivingHost(gel.firstEvent().e_receiving_host)
    gel.insertEvent(new_data_departure_event)


if __name__ == '__main__':
    gel = GlobalEventList()

    # event_type
    # 1  = arrival
    # 2  = departure
    # 3  = sensor
    # -1 = timeout

    # each host generates an arrival, sensor, then departure event

    all_hosts = list()

    for i in range(0, NUM_HOST):
        all_hosts.append(Host())
        new_event = Event()
        new_event.setEventType(1)  # arrival event
        new_event.setSecondaryEventType('starting arrival event of data frame')  # arrival event of data_frame --> sensor, departure event happens in processArrivalEvent fct
        new_event.setEventTime(TIME)  # arrival event time
        new_event.setEventSendingHost(i)  # arrival event is happening at host i

        dest_host = random.randint(1, NUM_HOST)  # destination host randomly generated
        while i == dest_host:  # destination host cannot be same as receiving host
            dest_host = random.randint(1, NUM_HOST)
        new_event.setEventReceivingHost(dest_host)  # arrival event destination host initialized
        gel.insertEvent(new_event)  # add to GEL

    # run through 100000 iterations

    for i in range(0, NUM_OF_FRAMES):

        time_difference = gel.firstEvent().eventTime() - TIME
        TIME = gel.firstEvent().eventTime()

        if gel.firstEvent().curEventType() == 1:  # arrival event
            processArrivalEvent(gel, all_hosts)

        elif gel.firstEvent().curEventType() == 2:  # departure event
            processDepartureEvent(gel, all_hosts)

        elif gel.firstEvent().curEventType() == 3:  # sensor event
            channelSensingEvent(gel, all_hosts)

        elif gel.firstEvent().curEventType() == -1:  # timeout SIFS
            variousTimers(gel, all_hosts)

        gel.removeFirstEvent()  # remove first event of GEL

    throughput = TOTAL_SUCCESSFULL_BYTES / TIME
    print 'time: %f' %TIME
    print 'total bytes %f' %TOTAL_SUCCESSFULL_BYTES

    trans_delay = 0
    queue_delay = 0
    for i in range(0, NUM_HOST):
        trans_delay += all_hosts[i].trans_delay
        queue_delay += all_hosts[i].queue_delay

    print 'Throughput = %.2f' % throughput
    print 'Average Network Delay = %.2f' % ((trans_delay + queue_delay)/ throughput)
