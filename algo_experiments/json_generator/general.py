import json


class General(object):
    def __init__(self):
        self.nodes = []
        self.links = []

    def addHost(self, name, cpu, memory):
        self.nodes.append((name, cpu, memory))

    def addLink(self, h1, h2, bandwidth):
        self.links.append((h1, h2, bandwidth))

    def build(self):
        total = {"nodes": [], "links": []}
        pool = iter(range(100000))
        for n, cpu, memory in self.nodes:
            node = {
                "id": n,
                "cores": cpu,
                "memory": memory
            }

            total["nodes"].append(node)

        for n1, n2, bw in self.links:
            inumber = next(pool)
            link_ = {
                "source": n1,
                "target": n2,
                "devices": [
                    {
                        "source_device": "eth{}".format(inumber),
                        "target_device": "eth{}".format(inumber),
                        "rate": bw
                    }
                ]
            }
            total["links"].append(link_)

        return json.dumps(total, indent=4, sort_keys=True)


def Lyon():
    topo = General()
    for i in range(1,5):
        h = "sagittaire-{}.lyon.grid5000.fr".format(i)
        topo.addHost(h,cpu=2, memory=1500)
        topo.addLink(h,"s1",bandwidth=1000)
        h = "hercule-{}.lyon.grid5000.fr".format(i)
        topo.addHost(h, cpu=24, memory=32000)
        topo.addLink(h, "s3",bandwidth=10000)
        h = "orion-{}.lyon.grid5000.fr".format(i)
        topo.addHost(h, cpu=24, memory=32000)
        topo.addLink(h, "s3", bandwidth=10000)

    topo.addHost("sagittaire-5.lyon.grid5000.fr", cpu=2, memory=1500)
    topo.addLink("sagittaire-5.lyon.grid5000.fr", "s1",bandwidth=1000)

    topo.addHost("nova-1.lyon.grid5000.fr", cpu=32, memory=64000)
    topo.addHost("nova-2.lyon.grid5000.fr", cpu=32, memory=64000)
    topo.addLink("nova-1.lyon.grid5000.fr", "s3", bandwidth=10000)
    topo.addLink("nova-2.lyon.grid5000.fr", "s3", bandwidth=10000)

    topo.addLink("s1", "s2", bandwidth=10000)
    topo.addLink("s2", "s3", bandwidth=10000)

    print(topo.build())


def Rennes():
    topo = General()
    topo.addHost("parapide-1.rennes.grid5000.fr", cpu=16, memory=24000)
    topo.addLink("parapide-1.rennes.grid5000.fr", "s1", bandwidth=1000)
    topo.addHost("parapide-10.rennes.grid5000.fr", cpu=16, memory=24000)
    topo.addLink("parapide-10.rennes.grid5000.fr", "s1", bandwidth=1000)
    for i in [1, 2, 9, 11, 12, 20, 21, 22]:
        host = "parapluie-{}.rennes.grid5000.fr".format(i)
        topo.addHost(host, cpu=24, memory=48000)
        topo.addLink(host, "s1", bandwidth=1000)
    for i in [1, 2, 3, 4, 5]:
        host = "parasilo-{}.rennes.grid5000.fr".format(i)
        topo.addHost(host, cpu=32, memory=128000)
        topo.addLink(host, "s2", bandwidth=10000)
    for i in [1,2,3,4,5]:
        host = "paravance-{}.rennes.grid5000.fr".format(i)
        topo.addHost(host, cpu=32, memory=128000)
        topo.addLink(host, "s3", bandwidth=10000)
    for i in [41,42,43,44,45]:
        host = "paravance-{}.rennes.grid5000.fr".format(i)
        topo.addHost(host, cpu=32, memory=128000)
        topo.addLink(host, "s4", bandwidth=10000)

    topo.addLink("s1", "s2", bandwidth=10000)
    topo.addLink("s2", "s3", bandwidth=40000)
    topo.addLink("s2", "s4", bandwidth=40000)
    print(topo.build())
    print(",".join([x[0] for x in topo.nodes]), "\t", len(topo.nodes))


if __name__ == '__main__':
    Rennes()

