import json


class Star(object):
    def __init__(self):
        pass

    @staticmethod
    def build(nodes, cpu=36, memory=96000, link=10000):
        total = {"nodes": [], "links": []}
        iface_number = 1
        for n in nodes:
            node = {
                "id": n,
                "cores": cpu,
                "memory": memory
            }

            total["nodes"].append(node)

            link_ = {
                "source": n,
                "target": "switch",
                "devices": [
                    {
                        "source_device": "eth0",
                        "target_device": "Ethernet{}".format(iface_number),
                        "rate": link
                    }
                ]
            }
            total["links"].append(link_)
            iface_number += 1

        return json.dumps(total, indent=4, sort_keys=True)


if __name__ == '__main__':
    nodes = ["grisou-{}.nancy.grid5000.fr".format(i) for i in range(11, 41)]
    nodes = [
        "gros-2.nancy.grid5000.fr",
"gros-3.nancy.grid5000.fr",
"gros-4.nancy.grid5000.fr",
"gros-5.nancy.grid5000.fr",
"gros-6.nancy.grid5000.fr",
"gros-20.nancy.grid5000.fr",
"gros-21.nancy.grid5000.fr",
"gros-22.nancy.grid5000.fr",
"gros-23.nancy.grid5000.fr",
"gros-24.nancy.grid5000.fr",
"gros-25.nancy.grid5000.fr",
"gros-26.nancy.grid5000.fr",
"gros-27.nancy.grid5000.fr",
"gros-28.nancy.grid5000.fr",
"gros-29.nancy.grid5000.fr",
"gros-30.nancy.grid5000.fr",
"gros-31.nancy.grid5000.fr",
"gros-32.nancy.grid5000.fr",
"gros-33.nancy.grid5000.fr",
"gros-34.nancy.grid5000.fr"
    ]
    print(Star.build(nodes=nodes, cpu=32, memory=96000, link=25000))
    print(",".join(nodes), len(nodes))


