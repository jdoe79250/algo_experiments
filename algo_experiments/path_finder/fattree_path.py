from .graph_converter import GraphConverted
from .OVSFlowConverter import OVSFlowConverter


class FatTreeConverted(GraphConverted):

    def __init__(self, g, net):
        super(FatTreeConverted, self).__init__(g, net)
        self.all_rules = None
        self.s_d = None

    def getRules(self):
        if self.all_rules:
            return self.all_rules, self.s_d

        net = self.getMininetNet()
        server_hosts = []
        client_hosts = []
        for h in net.hosts:
            if h.name.startswith("Hp"):
                client_hosts.append(h)
            elif h.name.startswith("Hsp"):
                server_hosts.append(h)
            else:
                err = "{} not a valid name for the fattree".format(h.name)
                raise ValueError(err)
        clients_name = [h.name for h in client_hosts]
        servers_name = [h.name for h in server_hosts]
        s_d = list(zip(clients_name, servers_name))
        switches = net.switches
        all_rules = {s.name: [] for s in switches}
        g_network = self.getNetwork()
        for source, destination in s_d:
            path = self.find_min_path(source, destination, weight="weight")
            weight = g_network[path[0]][path[1]]["weight"]
            self.update_path_weights(path=path, weight=weight)
            rules = self.path_rules(path=path)
            # removing the rules for the hosts
            rules.pop(path[0])
            rules.pop(path[-1])
            for s in rules:
                all_rules[s] = all_rules[s] + rules[s]

        self.all_rules = all_rules
        self.s_d = s_d
        return all_rules, s_d

    def update_path_weights(self, path, weight):
        if len(path) < 2:
            raise ValueError("the path should include at least 2 nodes")
        g = self._support_g
        g_ = self._total_bw_g
        for s, d in zip(path[:-1], path[1:]):
            g_[s][d]["weight"] += weight
            g.remove_edge(s, d)

    @staticmethod
    def getOVSRules(rules):
        ovs_rules = dict()
        for s in rules:
            list_rules = []
            for flow in rules[s]:
                ovs = OVSFlowConverter.create_rule(flow=flow)
                list_rules.append(ovs)
            ovs_rules[s] = list_rules[:]
        return ovs_rules


class HadoopFatTree(GraphConverted):

    def __init__(self, g, net):
        super(HadoopFatTree, self).__init__(g, net)
        self.all_rules = None
        self.s_d = None

    def getRules(self):
        print("****get rules***")
        if self.all_rules:
            return self.all_rules, self.s_d

        net = self.getMininetNet()
        s_d = [(u.name, v.name) for u in net.hosts for v in net.hosts]
        s_d = list(filter(lambda x: x[0] != x[1], s_d))
        s_d_ = []
        for u,v in s_d:
            if (u, v) in s_d_ or (v, u) in s_d_:
                pass
            else:
                s_d_.append((u,v))

        s_d = s_d_
        print(s_d)
        switches = net.switches
        all_rules = {s.name: [] for s in switches}
        g_network = self.getNetwork()
        for source, destination in s_d:
            print("finding {} {} path".format(source,destination))
            path = self.find_min_path(source, destination, weight="weight")
            weight = g_network[path[0]][path[1]]["weight"]
            self.update_path_weights(path=path, weight=weight)
            rules = self.path_rules(path=path)
            # removing the rules for the hosts
            rules.pop(path[0])
            rules.pop(path[-1])
            for s in rules:
                all_rules[s] = all_rules[s] + rules[s]

        self.all_rules = all_rules
        self.s_d = s_d
        return all_rules, s_d

    def update_path_weights(self, path, weight):
        if len(path) < 2:
            raise ValueError("the path should include at least 2 nodes")
        g = self._support_g
        g_ = self._total_bw_g
        for s, d in zip(path[:-1], path[1:]):
            g_[s][d]["weight"] += weight
            g[s][d]["weight"] += weight

    @staticmethod
    def getOVSRules(rules):
        ovs_rules = dict()
        for s in rules:
            list_rules = []
            for flow in rules[s]:
                ovs = OVSFlowConverter.create_rule(flow=flow)
                list_rules.append(ovs)
            ovs_rules[s] = list_rules[:]
        return ovs_rules

