from networkx import Graph
from networkx.algorithms.shortest_paths.generic import shortest_path
from abc import abstractmethod


class GraphConverted(object):

    def __init__(self, g, net):
        self._g = g
        self._net = net
        edges = [e for e in g.edges]
        w_edges = [(u, v, 1) for u, v in edges]
        self._support_g = Graph()
        self._support_g.add_weighted_edges_from(w_edges)
        w_edges = [(u, v, 0) for u, v in edges]
        self._total_bw_g = Graph()
        self._total_bw_g.add_weighted_edges_from(w_edges)

    def getNetwork(self):
        return self._g

    def getSupport(self):
        return self._support_g

    def getTotalBwNetwork(self):
        return self._total_bw_g

    def getMininetNet(self):
        return self._net

    @staticmethod
    def getNetworkPorts(net):
        ports = dict()
        links = net.links
        for link in links:
            node1, node2 = [intf.node.name for intf in
                            [link.intf1, link.intf2]]

            port1, port2 = [intf.name.split("-")[1][3:] for intf in
                            [link.intf1, link.intf2]]

            ports[(node1, node2)] = (port1, port2)
            ports[(node2, node1)] = (port2, port1)
        return ports

    @classmethod
    def from_mininet(cls, net):
        w_links = []
        for link in net.links:
            intf1, intf2 = link.intf1, link.intf2
            n1, n2 = intf1.node.name, intf2.node.name
            bw = 0
            if "bw" in intf1.params:
                bw = intf1.params["bw"]
            w_links.append((n1, n2, bw))
        g = Graph()
        g.add_weighted_edges_from(w_links)
        return cls(g, net)

    def find_min_path(self, source, dest, weight="weight"):
        g = self._support_g
        return shortest_path(g, source, dest, weight=weight)

    def update_path_weights(self, path, weight):
        if len(path) < 2:
            raise ValueError("the path should include at least 2 nodes")
        g = self._support_g
        g_ = self._total_bw_g
        for s, d in zip(path[:-1], path[1:]):
            g[s][d]["weight"] += weight
            g_[s][d]["weight"] += weight

    def path_rules(self, path):
        ports = self.getNetworkPorts(self._net)
        src_name = path[0]
        dst_name = path[-1]
        src = self._net.getNodeByName(src_name)
        dst = self._net.getNodeByName(dst_name)
        src_mac = src.MAC()
        dst_mac = dst.MAC()
        src_ip = src.IP()
        dst_ip = dst.IP()
        rules = dict()
        for u, v in zip(path[:-1], path[1:]):
            if u not in rules:
                rules[u] = []
            if v not in rules:
                rules[v] = []

            uport, vport = ports[(u, v)]
            rules[u].append({"src_ip": src_ip, "src_mac": src_mac,
                             "dst_ip": dst_ip, "dst_mac": dst_mac,
                             "out_port": uport})

            rules[v].append({"src_ip": dst_ip, "src_mac": dst_mac,
                             "dst_ip": src_ip, "dst_mac": src_mac,
                             "out_port": vport})
        return rules

    @abstractmethod
    def getRules(self):
        pass
