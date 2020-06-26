import unittest
from algo_experiments.path_finder import GraphConverted
from mininet.topo import Topo
from mininet.net import Mininet
from os import system


class MyTestCase(unittest.TestCase):

    def setUp(self):
        system("mn -c")

    def test_getports(self):
        topo = Topo()
        topo.addHost("h1")
        topo.addHost("h2")
        topo.addSwitch("s1")
        topo.addLink("h1", "s1", port1=20, port2=30)
        topo.addLink("h2", "s1", port1=10, port2=40)
        net = Mininet(topo=topo, controller=None, build=True)
        expected = {('h1', 's1'): ('20', '30'),
                    ('s1', 'h1'): ('30', '20'),
                    ('h2', 's1'): ('10', '40'),
                    ('s1', 'h2'): ('40', '10')}
        result = sorted(GraphConverted.getNetworkPorts(net=net).items())
        net.stop()
        self.assertEqual(sorted(expected.items()), result)

    def test_from_mininet_topo(self):
        topo = Topo()
        topo.addHost("h1")
        topo.addHost("h2")
        topo.addSwitch("s1")
        topo.addLink("h1", "s1", bw=10)
        topo.addLink("h2", "s1", bw=20)
        net = Mininet(topo=topo, controller=None, build=True)
        weigths = sorted([0, 0])
        result = GraphConverted.from_mininet(net=net)
        result = result.getTotalBwNetwork()
        g_edges = result.edges.data('weight', default=1)
        g_weigths = sorted([edge[2] for edge in g_edges])
        net.stop()
        self.assertEqual(weigths, g_weigths)

    def test_from_mininet_topo_1(self):
        topo = Topo()
        topo.addHost("h1")
        topo.addHost("h2")
        topo.addSwitch("s1")
        topo.addLink("h1", "s1")
        topo.addLink("h2", "s1")
        net = Mininet(topo=topo, controller=None, build=True)
        result = GraphConverted.from_mininet(net=net)
        result = result.getNetwork()
        g_edges = result.edges.data()
        net.stop()
        self.assertEqual(2, len(g_edges))

    def test_find_min_path(self):
        topo = Topo()
        topo.addHost("h1")
        topo.addHost("h2")
        topo.addSwitch("s1")
        topo.addLink("h1", "s1", bw=10)
        topo.addLink("h2", "s1", bw=20)
        net = Mininet(topo=topo, controller=None, build=True)
        result = GraphConverted.from_mininet(net=net)
        net.stop()
        expected = ['h1', 's1', 'h2']
        self.assertEqual(expected, result.find_min_path("h1", "h2"))

    def test_update_path_weights(self):
        topo = Topo()
        topo.addHost("h1")
        topo.addHost("h2")
        topo.addSwitch("s1")
        topo.addLink("h1", "s1", bw=10)
        topo.addLink("h2", "s1", bw=20)
        net = Mininet(topo=topo, controller=None, build=True)
        result = GraphConverted.from_mininet(net=net)
        result.update_path_weights(["h1", "s1", "h2"], weight=5)
        result = result.getSupport()
        g_edges = result.edges.data('weight', default=1)
        sum_weigths = sum([edge[2] for edge in g_edges])
        net.stop()
        self.assertEqual(12, sum_weigths)

    def test_update_path_weights_1(self):
        topo = Topo()
        topo.addHost("h1")
        topo.addHost("h2")
        topo.addSwitch("s1")
        topo.addLink("h1", "s1", bw=10)
        topo.addLink("h2", "s1", bw=20)
        net = Mininet(topo=topo, controller=None, build=True)
        result = GraphConverted.from_mininet(net=net)
        try:
            result.update_path_weights(["h1"], weight=5)
        except ValueError:
            net.stop()
            self.assertTrue(True)
        else:
            net.stop()
            self.assertTrue(False)

    def test_path_rules(self):
        topo = Topo()
        topo.addHost("h1", mac="00:00:00:00:00:01", ip="10.0.0.1/24")
        topo.addHost("h2", mac="00:00:00:00:00:02", ip="10.0.0.2/24")
        topo.addSwitch("s1")
        topo.addSwitch("s2")
        topo.addLink("h1", "s1", bw=10, port1=1, port2=3)
        topo.addLink("s1", "s2", bw=10, port1=2, port2=5)
        topo.addLink("s2", "h2", bw=20, port1=8, port2=10)
        expected_s1_paths = [{'src_ip': '10.0.0.1',
                              'src_mac': '00:00:00:00:00:01',
                              'dst_ip': '10.0.0.2',
                              'dst_mac': '00:00:00:00:00:02',
                              'out_port': '2'},
                             {'src_ip': '10.0.0.2',
                              'src_mac': '00:00:00:00:00:02',
                              'dst_ip': '10.0.0.1',
                              'dst_mac': '00:00:00:00:00:01',
                              'out_port': '3'}]

        expected_s2_paths = [{'src_ip': '10.0.0.1',
                              'src_mac': '00:00:00:00:00:01',
                              'dst_ip': '10.0.0.2',
                              'dst_mac': '00:00:00:00:00:02',
                              'out_port': '8'},
                             {'src_ip': '10.0.0.2',
                              'src_mac': '00:00:00:00:00:02',
                              'dst_ip': '10.0.0.1',
                              'dst_mac': '00:00:00:00:00:01',
                              'out_port': '5'}]

        net = Mininet(topo=topo, controller=None, build=True)
        result = GraphConverted.from_mininet(net=net)
        paths = result.path_rules(["h1", "s1", "s2", "h2"])
        s1, s2 = paths["s1"], paths["s2"]
        net.stop()
        for i in s1:
            if i["src_ip"] == '10.0.0.1':
                if i['out_port'] != "2":
                    self.assertTrue(False)
            if i["src_ip"] == '10.0.0.2':
                if i['out_port'] != "3":
                    self.assertTrue(False)

        for i in s2:
            if i["src_ip"] == '10.0.0.1':
                if i['out_port'] != "8":
                    self.assertTrue(False)
            if i["src_ip"] == '10.0.0.2':
                if i['out_port'] != "5":
                    self.assertTrue(False)

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
