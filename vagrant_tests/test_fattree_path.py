import unittest
from algo_experiments.path_finder.fattree_path import FatTreeConverted
from algo_experiments.fattree import FatTree
from mininet.net import Mininet
from os import system


class MyTestCase(unittest.TestCase):

    def setUp(self):
        system("mn -c")

    def test_getRules_1(self):
        topo = FatTree(k=2)
        net = Mininet(topo=topo, controller=None)
        ft = FatTreeConverted.from_mininet(net)
        rules, s_d = ft.getRules()
        net.stop()
        self.assertEqual(1, len(s_d))

    def test_getRules_2(self):
        topo = FatTree(k=4)
        net = Mininet(topo=topo, controller=None)
        ft = FatTreeConverted.from_mininet(net)
        rules, s_d = ft.getRules()
        net.stop()
        self.assertEqual(8, len(s_d))

    def test_getRules_3(self):
        topo = FatTree(k=6)
        net = Mininet(topo=topo, controller=None)
        ft = FatTreeConverted.from_mininet(net)
        rules, s_d = ft.getRules()
        net.stop()
        self.assertEqual(27, len(s_d))

    def test_getRules_4(self):
        topo = FatTree(k=8)
        net = Mininet(topo=topo, controller=None)
        ft = FatTreeConverted.from_mininet(net)
        rules, s_d = ft.getRules()
        net.stop()
        self.assertEqual(64, len(s_d))


if __name__ == '__main__':
    unittest.main()
