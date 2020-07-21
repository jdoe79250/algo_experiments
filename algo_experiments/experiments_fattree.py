from time import sleep
from algo_experiments.path_finder.fattree_path import FatTreeConverted, HadoopFatTree
from mininet.log import output, error
from mininet.cli import CLI
from pathlib import Path
import json
from algo_experiments.distrinet.mininet.mininet.dutil import makeFile, default_images
import re


path = "../results"
RESULTS_PATH = Path(path)
PHYSICAL = "gros"


def installArp(hs, hd):
    mac_s, ip_s = hs.MAC(), hs.IP()
    mac_d, ip_d = hd.MAC(), hd.IP()
    hs.setARP(ip=ip_d, mac=mac_d)
    hd.setARP(ip=ip_s, mac=mac_s)


def saveExperiments(experiment, path):
    with open(path, "w") as f:
        f.writelines(json.dumps(experiment, indent=4, sort_keys=True))


def iperf(net):
    ft = network_preparation(net=net, cls_=FatTreeConverted)
    output("******** IPERF {} ********\n".format(net.mapping_algo))
    rules, source_destination = ft.getRules()
    servers = [net.getNodeByName(s[0]) for s in source_destination]
    clients = [net.getNodeByName(d[1]) for d in source_destination]
    for dest in servers:
        dest.cmd("bash -c 'iperf -s &'")

    print("\n\n******* Starting EXP ***********")
    t = 60
    for src, dest in zip(clients, servers):
        file = "/tmp/{}_iperf.out".format(src.name)
        cmd = "bash -c 'iperf -t {} -c {} > {} &'".format(t,
                                                          dest.IP(),
                                                          file)
        src.cmd(cmd)
    sleep(t+3)

    results = dict()
    for src, dest in zip(clients, servers):
        out = src.cmd("cat /tmp/{}_iperf.out".format(src.name))
        results[src.name + "->" + dest.name] = net._parseIperf(out)

    Ks = {(k/2)**2 + k**2: k for k in range(2, 21, 2)}
    K = Ks[len(net.switches)]
    algo = net.mapping_algo
    name = "FT_K{}_Placer_{}_Physical_{}_iperf.exp".format(K, algo,
                                                       PHYSICAL)
    saveExperiments(experiment=results, path=RESULTS_PATH/name)
    output(results)


def aliasMaster(topo, net, master):
    output ("The Hadoop master is {}\n".format(master))

    lines = []
    line = "{} {}".format(net.nameToNode[master].IP(), "master")
    lines.append(line)
    for host in topo.hosts():
        lines.append("{} {}".format(net.nameToNode[host].IP(), host))
#    output (" >>> {}\n".format(lines))
    for host in topo.hosts():
#        output ("\t Adding to host {}".format(lines))
        makeFile(net=net, host=host, lines=lines, filename="/etc/hosts", overwrite=False)

def makeMaster(topo, net, master):
    """Generate the etc/hadoop/masters file on all the masters
    """
    makeFile(net, master, [master], "/root/hadoop-2.7.6/etc/hadoop/masters", overwrite=False)


def makeSlaves(topo, net, master, workers):
    """ Generate the etc/hadoop/slaves file on all hosts
    """
    cluster = [master] + workers
    slaves = workers

    """    hosts = topo.hosts()
    for host in hosts:
        if "role" in topo.nodeInfo(host).keys():
            if topo.nodeInfo(host)["role"] == "slave":
                slaves.append(host)
                cluster.append(host)
            elif topo.nodeInfo(host)["role"] == "master":
                cluster.append(host)"""

    # Execute the command to build etc/hadoop/slaves on each host
    for host in cluster:
        makeFile(net, host, slaves, "/root/hadoop-2.7.6/etc/hadoop/slaves", overwrite=False)

def parse_hadoop( Hadoopoutput):
    """Parse iperf output and return bandwidth.
       iperfOutput: string
       returns: result string"""
    r = r'Job Finished in [\d\.]+ seconds'
    m = re.findall( r, Hadoopoutput )
    if m:
        return m[0].split("in ")[1].split(" sec")[0]
    else:
        # was: raise Exception(...)
        error( 'could not parse Hadoop output: ' + Hadoopoutput )
        return ''
    pass

def hadoop(net):
    network_preparation(net=net, cls_=HadoopFatTree)
    output("******** HADOOP {} ********\n\n".format(net.mapping_algo))
    master_name = "Hp1e1s1"
    master = net.getNodeByName(master_name)
    workers = list(filter(lambda x: x.name != master_name, net.hosts))

    workers_names = [w.name for w in workers]

    topo = net.topo
    aliasMaster(topo=topo, net=net, master=master.name)
    output ("# populate etc/hadoop/masters\n")
    makeMaster(topo=topo, net=net, master=master.name)

    output ("# populate etc/hadoop/slaves\n")
    makeSlaves(topo=topo, net=net, master=master.name, workers=workers_names)

    hadoopMasterNode = master

    output ("# Start Hadoop in the cluster\n")
    output ("# Format HDFS\n")
    output (hadoopMasterNode.cmd('bash -c "/root/hadoop-2.7.6/bin/hdfs namenode -format -force"'))

    output ("# Launch HDFS\n")
    output (hadoopMasterNode.cmd('bash -c "/root/hadoop-2.7.6/sbin/start-dfs.sh"'))

    output ("# Launch YARN\n")
    output (hadoopMasterNode.cmd('bash -c "/root/hadoop-2.7.6/sbin/start-yarn.sh"'))

    output ("# Create a directory for the user\n")
    output (hadoopMasterNode.cmd('bash -c "/root/hadoop-2.7.6/bin/hdfs dfs -mkdir -p /user/root"'))
    sleep(3)
    output("\n")
    output("# Compute PI\n")

    print("\n\n******* Starting EXP ***********")
    compute_output = hadoopMasterNode.cmd('bash -c "/root/hadoop-2.7.6/bin/hadoop jar  /root/hadoop-2.7.6/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.6.jar pi 2000 1000"')
    output(compute_output)
    job_completion_time = parse_hadoop(compute_output)

    Ks = {(k/2)**2 + k**2: k for k in range(2, 21, 2)}
    K = Ks[len(net.switches)]
    algo = net.mapping_algo
    name = "FT_K{}_Placer_{}_Physical_{}_hadoop.exp".format(K, algo,
                                                                  PHYSICAL)
    results = {"Hadoop_time": job_completion_time}
    saveExperiments(experiment=results, path=RESULTS_PATH/name)
    sleep(2)


def hadoop_mem(net):
    network_preparation(net=net, cls_=HadoopFatTree)
    output("******** HADOOP {} ********\n\n".format(net.mapping_algo))
    master_name = "Hp1e1s1"
    master = net.getNodeByName(master_name)
    workers = list(filter(lambda x: x.name != master_name, net.hosts))

    workers_names = [w.name for w in workers]

    topo = net.topo
    aliasMaster(topo=topo, net=net, master=master.name)
    output ("# populate etc/hadoop/masters\n")
    makeMaster(topo=topo, net=net, master=master.name)

    output ("# populate etc/hadoop/slaves\n")
    makeSlaves(topo=topo, net=net, master=master.name, workers=workers_names)

    hadoopMasterNode = master
    Ks = {(k / 2) ** 2 + k ** 2: k for k in range(2, 21, 2)}
    K = Ks[len(net.switches)]
    output ("# Start Hadoop in the cluster\n")
    output ("# Format HDFS\n")
    RAMDISKSIZE = 50
    for h in net.hosts:
        h.cmd('bash -c "mkdir /root/ramdisk/"')
        h.cmd('bash -c "mount -t tmpfs -o size={}g tmpfs /root/ramdisk/"'.format(RAMDISKSIZE))
        #h.cmd("""bash -c "sed -i 's/\/root\/datanode/\/root\/ramdisk\/datanode/g' /root/hadoop-2.7.6/etc/hadoop/hdfs-site.xml" """)

    #hadoopMasterNode.cmd("""bash -c "sed -i 's/\/root\/namenode/\/root\/ramdisk\/namenode/g' /root/hadoop-2.7.6/etc/hadoop/hdfs-site.xml" """)

    output (hadoopMasterNode.cmd('bash -c "/root/hadoop-2.7.6/bin/hdfs namenode -format -force"'))

    output ("# Launch HDFS\n")
    output (hadoopMasterNode.cmd('bash -c "/root/hadoop-2.7.6/sbin/start-dfs.sh"'))

    output ("# Launch YARN\n")
    output (hadoopMasterNode.cmd('bash -c "/root/hadoop-2.7.6/sbin/start-yarn.sh"'))

    output ("# Create a directory for the user\n")
    output (hadoopMasterNode.cmd('bash -c "/root/hadoop-2.7.6/bin/hdfs dfs -mkdir -p /user/root"'))
    sleep(3)
    output("\n")
    output("# Simulate In-Memory files\n")
    for h in net.hosts:
        h.cmd('bash -c "fallocate -l {}G /root/ramdisk/file"'.format(RAMDISKSIZE-2))

    print("\n\n******* Starting EXP  ***********")

    compute_output = hadoopMasterNode.cmd('bash -c "/root/hadoop-2.7.6/bin/hadoop jar  /root/hadoop-2.7.6/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.6.jar pi 2000 1000"')
    output(compute_output)
    sleep(10)

    job_completion_time = parse_hadoop(compute_output)


    algo = net.mapping_algo
    name = "FT_K{}_Placer_{}_Physical_{}_memory.exp".format(K, algo,
                                                              PHYSICAL)
    results = {"Hadoop_time": job_completion_time}
    saveExperiments(experiment=results, path=RESULTS_PATH/name)
    sleep(2)




def network_preparation(net, cls_=FatTreeConverted):
    output("******** PREPARING THE NETWORK {} ********\n".format(net.mapping_algo))
    ft = cls_.from_mininet(net)
    rules, source_destination = ft.getRules()
    ovs_rules = ft.getOVSRules(rules=rules)
    for switch in net.switches:
        print("installing {} rules ".format(switch.name))
        rl = ovs_rules[switch.name]
        for r in rl:
            cmd = "bash -c 'ovs-ofctl add-flow {} {}'".format(switch.name, r)
            switch.cmd(cmd)
    output(ovs_rules)

    for s, d in source_destination:
        installArp(net.getNodeByName(s), net.getNodeByName(d))
        output(s, d)
        ploss = net.ping([net.getNodeByName(s), net.getNodeByName(d)])
        if ploss != 0:
            print("PACKET LOSS !!!")
            return
        output()
    return ft

def toHadoop(topo):
    slave_image = 'ubuntu-hadoop-slave'
    master_image = 'ubuntu-hadoop-master'
    master = "Hp1e1s1"
    for host in topo.hosts(sort=True):
        image = master_image if host == master else slave_image
        infos = {}
        infos.update(topo.nodeInfo(host))
        infos.update({"image": image})
        topo.setNodeInfo(host, infos)


PREBUILD = [default_images, toHadoop]
#PREBUILD = [default_images]
tests = {"piperf": iperf, "hadoop": hadoop, "memory": hadoop_mem}
