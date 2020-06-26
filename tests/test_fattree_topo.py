import unittest

from algo_experiments.fattree import FatTree
from mininet.topo import Topo


class MyTestCase(unittest.TestCase):
    def test_instanceType(self):
        net = FatTree(4)
        self.assertTrue(issubclass(type(net), Topo))

    def test_hostNumber(self):
        k = 2
        net = FatTree(k)
        hosts = len(net.hosts())
        self.assertEqual((((k / 2) ** 2) * k), hosts)

    def test_hostNumber_1(self):
        k = 6
        net = FatTree(k)
        hosts = len(net.hosts())
        self.assertEqual((((k / 2) ** 2) * k), hosts)

    def test_assertOddK(self):
        k = 3
        try:
            FatTree(k)
        except Exception:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_linkNumber(self):
        k = 6
        net = FatTree(k)
        links = len(net.links())
        exp_links = ((k / 2) ** 2) * k * 2 + k * ((k / 2) ** 2)
        self.assertEqual(exp_links, links)


if __name__ == '__main__':
    unittest.main()
