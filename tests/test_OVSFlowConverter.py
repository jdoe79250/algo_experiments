import unittest
from algo_experiments.path_finder.OVSFlowConverter import OVSFlowConverter


class MyTestCase(unittest.TestCase):
    def test_create_rule(self):
        flow = {'src_ip': '10.0.0.1',
                'src_mac': '00:00:00:00:00:01',
                'dst_ip': '10.0.0.2',
                'dst_mac': '00:00:00:00:00:02',
                'out_port': '2'}

        expected_rule = "table=0,priority=10," \
                        "dl_src=00:00:00:00:00:01," \
                        "dl_dst=00:00:00:00:00:02," \
                        "ip," \
                        "ip_src=10.0.0.1," \
                        "ip_dst=10.0.0.2," \
                        "actions=output:2"

        self.assertEqual(expected_rule, OVSFlowConverter.create_rule(flow))

    def test_create_rule_1(self):
        flow = {'src_mac': '00:00:00:00:00:01',
                'dst_mac': '00:00:00:00:00:02',
                'out_port': '2'}

        expected_rule = "table=0,priority=10," \
                        "dl_src=00:00:00:00:00:01," \
                        "dl_dst=00:00:00:00:00:02," \
                        "actions=output:2"

        self.assertEqual(expected_rule, OVSFlowConverter.create_rule(flow))

    def test_create_rule_2(self):
        flow = {'dst_mac': '00:00:00:00:00:02',
                'out_port': '3'}

        expected_rule = "table=0,priority=10," \
                        "dl_dst=00:00:00:00:00:02," \
                        "actions=output:3"
        self.assertEqual(expected_rule, OVSFlowConverter.create_rule(flow))

    def test_create_rule_3(self):
        flow = {'dst_mac': '00:00:00:00:00:02'}

        expected_rule = "table=0,priority=10," \
                        "dl_dst=00:00:00:00:00:02," \
                        "actions=DROP"
        self.assertEqual(expected_rule, OVSFlowConverter.create_rule(flow))

    def test_create_rule_4(self):
        flow = {'dst_mac': '00:00:00:00:00:02',
                'priority': 30}

        expected_rule = "table=0,priority=30," \
                        "dl_dst=00:00:00:00:00:02," \
                        "actions=DROP"
        self.assertEqual(expected_rule, OVSFlowConverter.create_rule(flow))

    def test_create_rule_5(self):
        flow = {'src_ip': '10.0.0.1',
                'dst_ip': '10.0.0.2',
                'out_port': '2'}

        expected_rule = "table=0,priority=10," \
                        "ip," \
                        "ip_src=10.0.0.1," \
                        "ip_dst=10.0.0.2," \
                        "actions=output:2"
        self.assertEqual(expected_rule, OVSFlowConverter.create_rule(flow))

    def test_create_rule_6(self):
        flow = {}
        expected_rule = "table=0,priority=10,actions=DROP"
        self.assertEqual(expected_rule, OVSFlowConverter.create_rule(flow))

    def test_create_rule_7(self):
        flow = {"table": 2}
        expected_rule = "table=2,priority=10,actions=DROP"
        self.assertEqual(expected_rule, OVSFlowConverter.create_rule(flow))

    def test_create_rule_8(self):
        flow = {"in_port": 2, "out_port": 2}
        expected_rule = "table=0,priority=10,actions=output:IN_PORT"
        self.assertEqual(expected_rule, OVSFlowConverter.create_rule(flow))


if __name__ == '__main__':
    unittest.main()
