import network_3 as network
import link_3 as link
import threading
from time import sleep

##configuration parameters
router_queue_size = 0  # 0 means unlimited
simulation_time = 3  # give the network sufficient time to transfer all packets before quitting


if __name__ == '__main__':
    object_L = []  # keeps track of objects, so we can kill their threads

    # create network nodes
    #client = network.Host(1)
    #object_L.append(client)
    #server = network.Host(2)
    #object_L.append(server)
    #router_a = network.Router(name='A', intf_count=1, max_queue_size=router_queue_size)
    #object_L.append(router_a)

    client1 = network.Host(1)
    object_L.append(client1)

    client2 = network.Host(2)
    object_L.append(client2)

    server3 = network.Host(3)
    object_L.append(server3)

    server4 = network.Host(4)
    object_L.append(server4)

    router_a = network.Router(name='A', intf_count=1, max_queue_size=router_queue_size)
    object_L.append(router_a)

    router_b = network.Router(name='B', intf_count=1, max_queue_size=router_queue_size)
    object_L.append(router_b)

    router_c = network.Router(name='C', intf_count=1, max_queue_size=router_queue_size)
    object_L.append(router_c)

    router_d = network.Router(name='D', intf_count=1, max_queue_size=router_queue_size)
    object_L.append(router_d)



    # create a Link Layer to keep track of links between network nodes
    link_layer = link.LinkLayer()
    object_L.append(link_layer)

    # add all the links
    # link parameters: from_node, from_intf_num, to_node, to_intf_num, mtu
    #link_layer.add_link(link.Link(client, 0, router_a, 0, 50))
    #link_layer.add_link(link.Link(router_a, 0, server, 0, 10))

    link_layer.add_link(link.Link(client1, 0, router_a, 0, 50))
    link_layer.add_link(link.Link(client2, 0, router_a, 0, 50))
    link_layer.add_link(link.Link(router_a, 0, router_b, 0, 50))
    link_layer.add_link(link.Link(router_a, 0, router_c, 0, 50))
    link_layer.add_link(link.Link(router_b, 0, router_d, 0, 50))
    link_layer.add_link(link.Link(router_c, 0, router_d, 0, 50))
    link_layer.add_link(link.Link(router_d, 0, server3, 0, 50))
    link_layer.add_link(link.Link(router_d, 0, server4, 0, 50))

    # start all the objects
    thread_L = []
    #thread_L.append(threading.Thread(name=client.__str__(), target=client.run))
    #thread_L.append(threading.Thread(name=server.__str__(), target=server.run))
    #thread_L.append(threading.Thread(name=router_a.__str__(), target=router_a.run))

    thread_L.append(threading.Thread(name=client1.__str__(), target=client1.run))
    thread_L.append(threading.Thread(name=client2.__str__(), target=client2.run))

    thread_L.append(threading.Thread(name=server3.__str__(), target=server3.run))
    thread_L.append(threading.Thread(name=server4.__str__(), target=server4.run))

    thread_L.append(threading.Thread(name=router_a.__str__(), target=router_a.run))
    thread_L.append(threading.Thread(name=router_b.__str__(), target=router_b.run))
    thread_L.append(threading.Thread(name=router_c.__str__(), target=router_c.run))
    thread_L.append(threading.Thread(name=router_d.__str__(), target=router_d.run))

    thread_L.append(threading.Thread(name="Network", target=link_layer.run))

    for t in thread_L:
        t.start()

    # create some send events
    #for i in range(3):
    #    client.udt_send(2, 'Sample data %d' % i)

    client1.udt_send(3, "testing send to 3")

    #client.udt_send(2, 'first1234_second123_third1234_fourth123_fifth1234_sixth1234_seventh12_eighth123_')

    # give the network sufficient time to transfer all packets before quitting
    sleep(simulation_time)

    # join all threads
    for o in object_L:
        o.stop = True
    for t in thread_L:
        t.join()

    print("All simulation threads joined")

# writes to host periodically