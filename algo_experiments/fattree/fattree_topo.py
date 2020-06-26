from mininet.topo import Topo


def int2dpid(dpid):
    try:
        dpid = hex(dpid)[2:]
        dpid = '0' * (16 - len(dpid)) + dpid
        return dpid
    except IndexError:
        raise Exception('Unable to derive default datapath ID - '
                        'please either specify a dpid or use a '
                        'canonical switch name such as s23.')


def irange(start, end):
    return range(start, end + 1)


class FT(Topo):
    def coreName(self, seq):
        return "Cs%d" % seq

    def aggrName(self, pod, seq):
        return "Ap%ds%d" % (pod, seq)

    def edgeName(self, pod, seq):
        return "Ep%ds%d" % (pod, seq)

    def hostName(self, pod, edge, seq):
        name = "Hp%de%ds%d" % (pod, edge, seq)
        return name

    def serverName(self, pod, edge, seq):
        name = "Hsp%de%ds%d" % (pod, edge, seq)
        return name

    def makeDPID(self, i):
        return "0" * 10 + str(i)

    def build(self, k=4, bw=1000, host_cores=1, host_memory=1, switch_cores=1, switch_memory=1, **opts):
        dpid_ = 0
        if k % 2 != 0:
            raise Exception("k must be a multiple of 2")
        switch_mem = "{}GB".format(switch_memory)
        host_mem = "{}GB".format(host_memory)
        self.k = k
        k2 = int(k / 2)  # k/2
        switch_core_number = int((k / 2) ** 2)

        # build cores
        for seq in irange(1, switch_core_number):
            corename = self.coreName(seq)
            self.addSwitch(corename, dpid=self.makeDPID(dpid_), cpu=switch_cores, memory=switch_mem)
            dpid_ += 1

        # Create Pods
        l_ip = 1
        for pod in irange(1, k):

            # Create aggregation switches
            for aggr in irange(1, k2):
                aggrname = self.aggrName(pod, aggr)
                self.addSwitch(aggrname, dpid=self.makeDPID(dpid_), cpu=switch_cores, memory=switch_mem)
                dpid_ = dpid_ + 1

                # Connect it to the core switches
                for meta_pod in irange(1, k2):
                    coreid = (meta_pod - 1) * k2 + aggr
                    corename = self.coreName(coreid)
                    self.addLink(aggrname, corename, bw=bw)

            # Create edge switches
            for edge in irange(1, k2):
                edgename = self.edgeName(pod, edge)
                self.addSwitch(edgename, dpid=self.makeDPID(dpid_), cpu=switch_cores, memory=switch_mem)
                dpid_ = dpid_ + 1

                # Connect it to the aggregation switches
                for aggr in irange(1, k2):
                    self.addLink(edgename, self.aggrName(pod, aggr), bw=bw)

                # Create hosts

                for host in irange(1, k2):
                    if pod > k2:
                        hostname = self.serverName(pod, edge, host)
                    else:
                        hostname = self.hostName(pod, edge, host)
                    ip = "10.0.1.{}".format(l_ip)
                    mac = "00:00:00:00:01:"
                    mac += "{0:#0{1}x}".format(l_ip, 4)[2:]
                    self.addHost(hostname, ip=ip, mac=mac, cpu=host_cores, memory=host_mem)

                    # Connect it to the edge switch
                    self.addLink(hostname, edgename, bw=bw)
                    l_ip += 1

        # Verify the number of hosts, should be k * ((k/2)**2)
        assert (len(self.hosts()) == ((k / 2) ** 2) * k)

        # Verify the number of switches, should be
        #               (k/2)**2 cores + (k*k/2) aggr. + (k*k/2) edge.
        assert (len(self.switches()) == (k / 2) ** 2 + k * (k / 2 + k / 2))


topos = {"ft": FT}
