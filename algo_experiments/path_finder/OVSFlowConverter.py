from os import system


class OVSFlowConverter(object):
    def __init__(self):
        pass

    @staticmethod
    def create_rule(flow):
        rule = ""

        src_ip = flow["src_ip"] if "src_ip" in flow else None
        dst_ip = flow["dst_ip"] if "dst_ip" in flow else None
        src_mac = flow["src_mac"] if "src_mac" in flow else None
        dst_mac = flow["dst_mac"] if "dst_mac" in flow else None
        table = flow["table"] if "table" in flow else "0"
        out_port = flow["out_port"] if "out_port" in flow else None
        in_port = flow["in_port"] if "in_port" in flow else None
        priority = flow["priority"] if "priority" in flow.keys() else "10"

        rule = OVSFlowConverter.add_table(rule=rule, table_number=table)
        rule = OVSFlowConverter.add_priority(rule=rule, priority=priority)
        rule = OVSFlowConverter.add_mac_src_match(rule=rule,
                                                  mac_address=src_mac)
        rule = OVSFlowConverter.add_mac_dst_match(rule=rule,
                                                  mac_address=dst_mac)

        if src_ip or dst_ip:
            rule += ",ip"

        rule = OVSFlowConverter.add_ip_src_match(rule=rule, ip_address=src_ip)
        rule = OVSFlowConverter.add_ip_dst_match(rule=rule, ip_address=dst_ip)
        rule += ",actions="
        if out_port is None:
            rule += "DROP"
        else:
            rule = OVSFlowConverter.add_port_out_action(rule=rule,
                                                        port_number=out_port,
                                                        port_in=in_port)

        return rule

    def install_single_rule(self, switch, flow):
        command = "ovs-ofctl -O OpenFlow13 add-flow"
        system('{} {} "{}"'.format(command, switch, self.create_rule(flow)))

    @staticmethod
    def add_priority(rule, priority=None):
        if not priority:
            return rule
        return "{},{}{}".format(rule, "priority=", priority)

    @staticmethod
    def add_ip_src_match(rule, ip_address):
        if not ip_address:
            return rule
        return "{},{}{}".format(rule, "ip_src=", ip_address)

    @staticmethod
    def add_vlan_in_match(rule, vlan_number=None):
        if not vlan_number:
            return rule
        return "{},{}{}".format(rule, "dl_vlan=", vlan_number)

    @staticmethod
    def add_table(rule, table_number):
        if not table_number:
            table_number = "0"
        return "{}{}{}".format(rule, "table=", table_number)

    @staticmethod
    def add_ip_dst_match(rule, ip_address):
        if not ip_address:
            return rule
        return "{},{}{}".format(rule, "ip_dst=", ip_address)

    @staticmethod
    def add_mac_dst_match(rule, mac_address):
        if not mac_address:
            return rule
        return "{},{}{}".format(rule, "dl_dst=", mac_address)

    @staticmethod
    def add_mac_src_match(rule, mac_address):
        if not mac_address:
            return rule
        return "{},{}{}".format(rule, "dl_src=", mac_address)

    @staticmethod
    def add_vlan_out_action(rule, vlan_number, vlan_in=None):
        if vlan_number == vlan_in:
            """vlan are the same, it does not have to update the rule"""
            return rule
        if vlan_number == "pop" or (vlan_in and not vlan_number):
            """ in case of 'pop' or in case the vlan in input is setted
             while the vlan output action is not, the action remove
             the vlan field """

            return "{}{},".format(rule, "pop_vlan")

        if not vlan_in and vlan_number:
            """ in case vlan field in input is not setted and the vlan
                action output is setted, the action output has to create
                a vlan field """

            return "{}{}{}{},".format(rule,
                                      "push_vlan:0x8100,set_field:",
                                      int(vlan_number) + 4096,
                                      "->vlan_vid")

        if vlan_number != vlan_in:
            "the action has to update the vlan field"
            return "{}{}{}{},".format(rule, "set_field:",
                                      int(vlan_number) + 4096,
                                      "->vlan_vid")

    @staticmethod
    def add_port_out_action(rule, port_number, port_in=None):
        if not port_number:
            return rule
        if port_number == port_in:
            return "{}{}{}".format(rule, "output:", "IN_PORT")
        else:
            return "{}{}{}".format(rule, "output:", port_number)
