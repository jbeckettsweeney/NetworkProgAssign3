import queue
import threading
from time import sleep
import random


## wrapper class for a queue of packets
class Interface:
    ## @param maxsize - the maximum size of the queue storing packets
    def __init__(self, maxsize=0):
        self.queue = queue.Queue(maxsize);
        self.mtu = None

    ##get packet from the queue interface
    def get(self):
        try:
            return self.queue.get(False)
        except queue.Empty:
            return None

    ##put the packet into the interface queue
    # @param pkt - Packet to be inserted into the queue
    # @param block - if True, block until room in queue, if False may throw queue.Full exception
    def put(self, pkt, block=False):
        self.queue.put(pkt, block)


## Implements a network layer packet (different from the RDT packet
# from programming assignment 2).
# NOTE: This class will need to be extended to for the packet to include
# the fields necessary for the completion of this assignment.
class NetworkPacket:
    ## packet encoding lengths
    dst_addr_S_length = 3
    srcAddrLength = 2

    ##@param dst_addr: address of the destination host
    # @param data_S: packet payload
    def __init__(self, dst_addr, srcAddr, data_S):
        sleep(random.random()/4)
        self.dst_addr = dst_addr
        self.srcAddr = srcAddr
        self.data_S = data_S

    ## called when printing the object
    def __str__(self):
        return self.to_byte_S()

    ## convert packet to a byte string for transmission over links
    def to_byte_S(self):
        sleep(random.random()/4)
        byte_S = str(self.dst_addr).zfill(self.dst_addr_S_length)
        byte_S += str(self.srcAddr).zfill(self.srcAddrLength)
        byte_S += self.data_S
        return byte_S

    ## extract a packet object from a byte string
    # @param byte_S: byte string representation of the packet
    @classmethod
    def from_byte_S(self, byte_S):
        dst_addr = int(byte_S[0: NetworkPacket.dst_addr_S_length])
        srcAddr = int(byte_S[NetworkPacket.dst_addr_S_length: (NetworkPacket.dst_addr_S_length + NetworkPacket.srcAddrLength)])
        data_S = byte_S[(NetworkPacket.dst_addr_S_length + NetworkPacket.srcAddrLength):]
        return self(dst_addr, srcAddr, data_S)


## Implements a network host for receiving and transmitting data
class Host:

    ##@param addr: address of this node represented as an integer
    def __init__(self, addr):
        self.addr = addr
        self.in_intf_L = [Interface()]
        self.out_intf_L = [Interface()]
        self.stop = False  # for thread termination

    ## called when printing the object
    def __str__(self):
        return 'Host_%s' % (self.addr)

    ## create a packet and enqueue for transmission
    # @param dst_addr: destination address for the packet
    # @param data_S: data being transmitted to the network layer
    def udt_send(self, dst_addr, srcAddr, data_S):
        sleep(random.random()/4)
        p = NetworkPacket(dst_addr, srcAddr, data_S)
        self.out_intf_L[0].put(p.to_byte_S())  # send packets always enqueued successfully
        print()
        print('%s: sending packet "%s" on the out interface with mtu=%d' % (self, p, self.out_intf_L[0].mtu))
        print()

    ## receive packet from the network layer
    def udt_receive(self):
        sleep(random.random()/4)
        pkt_S = self.in_intf_L[0].get()
        if pkt_S is not None:
            print()
            print('%s: received packet "%s" on the in interface' % (self, pkt_S))
            print()

    ## thread target for the host to keep receiving data
    def run(self):
        print()
        print(threading.currentThread().getName() + ': Starting')
        print()
        while True:
            # receive data arriving to the in interface
            self.udt_receive()
            # terminate
            if (self.stop):
                print()
                print(threading.currentThread().getName() + ': Ending')
                print()
                return


## Implements a multi-interface router described in class
class Router:

    ##@param name: friendly router name for debugging
    # @param intf_count: the number of input and output interfaces
    # @param max_queue_size: max queue length (passed to Interface)
    def __init__(self, name, intf_count, max_queue_size):
        self.stop = False  # for thread termination
        self.name = name
        # create a list of interfaces
        self.in_intf_L = [Interface(max_queue_size) for _ in range(intf_count)]
        self.out_intf_L = [Interface(max_queue_size) for _ in range(intf_count)]

    ## called when printing the object
    def __str__(self):
        return 'Router_%s' % (self.name)

    ## look through the content of incoming interfaces and forward to
    # appropriate outgoing interfaces
    def forward(self):
        sleep(random.random()/4)
        for i in range(len(self.in_intf_L)):
            pkt_S = None
            try:
                # get packet from interface i
                pkt_S = self.in_intf_L[i].get()
                # if packet exists make a forwarding decision
                if pkt_S is not None:
                    p = NetworkPacket.from_byte_S(pkt_S)  # parse a packet out
                    address = p.dst_addr
                    source = p.srcAddr
                    print()
                    print("p.address = ", address)
                    print("p.source = ", source)
                    print("self.name = ", self.name)
                    print()
                    # HERE you will need to implement a lookup into the
                    # forwarding table to find the appropriate outgoing interface
                    # for now we assume the outgoing interface is also i

                    #routing table
                    if (self.name == "A"):
                        print("we are in A")
                        if (source == 1):
                            self.out_intf_L[0].put(p.to_byte_S(), True)
                            print("sending to interface 0")
                        elif (source == 2):
                            self.out_intf_L[1].put(p.to_byte_S(), True)
                            print("sending to interface 1")
                        else:
                            print("source didn't match 1 or 2")
                            self.out_intf_L[i].put(p.to_byte_S(), True)
                    elif (self.name == "D"):
                        print("we are in D")
                        if (address == 3):
                            self.out_intf_L[0].put(p.to_byte_S(), True)
                            print("sending to interface 0")
                        elif (address == 4):
                            self.out_intf_L[1].put(p.to_byte_S(), True)
                            print("sending to interface 1")
                        else:
                            print("source didn't match 1 or 2")
                            self.out_intf_L[i].put(p.to_byte_S(), True)
                    else:
                        print("we are not in A or D")
                        self.out_intf_L[i].put(p.to_byte_S(), True)

            except queue.Full:
                print()
                print('%s: packet "%s" lost on interface %d' % (self, p, i))
                print()
                pass
    print()
    ## thread target for the host to keep forwarding data
    def run(self):
        print()
        print(threading.currentThread().getName() + ': Starting')
        print()
        while True:
            self.forward()
            if self.stop:
                print()
                print(threading.currentThread().getName() + ': Ending')
                print()
                return