from unittest import TestCase
from algo_experiments.json_generator import Star
import json


class TestStar(TestCase):
    def test_build_1(self):
        nodes = ["n1", "n2", "n3"]
        star = Star.build(nodes=nodes, cpu=10, memory=100, link=1000)
        star = eval(star)
        self.assertEqual(3, len(star["nodes"]))

    def test_build_2(self):
        nodes = ["n1", "n2", "n3"]
        star = Star.build(nodes=nodes, cpu=10, memory=100, link=1000)
        star = eval(star)
        self.assertEqual(3, len(star["links"]))

    def test_build_3(self):
        nodes = ["n1", "n2", "n3"]
        star = Star.build(nodes=nodes, cpu=10, memory=100, link=1000)
        star = eval(star)
        result = [n["id"] for n in star["nodes"]]
        self.assertEqual(["n1", "n2", "n3"], sorted(result))
