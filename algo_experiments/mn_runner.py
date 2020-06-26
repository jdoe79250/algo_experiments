from mininet.link import TCLink
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import output
from mininet.node import OVSSwitch, RemoteController
from mininet.topo import LinearTopo

from algo_experiments.fattree import FatTree
from os import system
from algo_experiments.path_finder.fattree_path import FatTreeConverted
from time import sleep
from algo_experiments.experiments_fattree import iperf


def run():
    topo = FatTree(6)
    net = Mininet(topo=topo, link=TCLink, controller=None)
    net.start()
    # sleep(5)
    # Mininet API for the experiment
    #  sysctl -w net.ipv4.neigh.default.gc_thresh1=4098
    # increase the arp table cache
    print("ARP TABLES")

    net.staticArp()
    ft = FatTreeConverted.from_mininet(net)
    rules, s_d = ft.getRules()
    ovs_rules = ft.getOVSRules(rules=rules)
    for switch in net.switches:
        print(switch.name)
        rl = ovs_rules[switch.name]
        for r in rl:
            cmd = "bash -c 'ovs-ofctl add-flow {} {}'".format(switch.name, r)
            print(switch.name, cmd)
            switch.cmd(cmd)
        print()
    print(ovs_rules)
    # Run the CLI
    for s, d in s_d:
        print(s, d)
        ploss = net.ping([net.getNodeByName(s), net.getNodeByName(d)])
        if ploss > 0:
            print(s, d, "PACKET LOSS!")
            break
        print(ploss)

    results = iperf(net, s_d)
    print(results)

    CLI(net)
    net.stop()


if __name__ == '__main__':
    run()
