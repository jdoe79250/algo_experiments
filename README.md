# Run the Client
To run the Distrinet client, you can clone this repository and run Vagrant.


```bash
git clone https://github.com/jdoe79250/algo_experiments.git
cd algo_experiments
vagrant up
```
after few minutes, the vm should be running, you can connect to it with:

```bash
vagrant ssh
```
The environment will not configure a physical infrastructure for you.
To install the environment you can follow the official Distrinet website:

https://distrinet-emu.github.io

https://distrinet-emu.github.io/general_environment.html

Following the tutorial, you can runa the example using the default RoundRobin Mapper with:

```bash
ryu-manager /usr/lib/python3/dist-packages/ryu/app/simple_switch_13.py --verbose
```

as explained in the tutorial

# Physical environment mapping

for the new algorithm implemented, you have to create the file description of this infrastructure.
The vagrant VM create an example environment.

The example file describe an infrastructure composed by 2 physical machines with IP_1=192.168.0.10 ip_2=192.168.0.11, connected with one switch sw1.

The example file is located at:

```bash
/home/vagrant/.distrinet/simple_environment.json
```

You can adapt this file for your infrastructure.

# Run network experiment
For Network experiment you have to enable the PREBUILD = [default_images] command in the file "/vagrant/algo_experiments/experiments_fattree.py"


This command will run the network experiment in FatTree topology, K=4 and links at 500mbps, all the vNodes requires 1 vCore and 2Gb of RAM
```bash
bin/dmn --controller lxcremote,ip=192.168.0.1 --bastion="192.168.0.10" --workers="192.168.0.10,192.168.0.11"  --custom=/vagrant/algo_experiments/fattree/fattree_topo.py,/vagrant/algo_experiments/experiments_fattree.py  --test piperf --topo ft,4,500,1,2,1,2
```

# Run CPU experiment
For CPU and Memory experiment you have to enable the PREBUILD = [default_images, toHadoop] command in the file "/vagrant/algo_experiments/experiments_fattree.py"

This command will run the network experiment in FatTree topology, K=4 and links at 500mbps, all the vHosts requires 8 vCore and 12 Gb of RAM, while the vSwitch requires 1vCpu and 2 GB of RAM

```bash
bin/dmn --controller lxcremote,ip=192.168.0.1 --bastion="192.168.0.10" --workers="192.168.0.10,192.168.0.11"  --custom=/vagrant/algo_experiments/fattree/fattree_topo.py,/vagrant/algo_experiments/experiments_fattree.py  --test hadoop --topo ft,4,500,8,12,1,2
```

# Run Memory experiment

This command will run the network experiment in FatTree topology, K=4 and links at 500mbps, all the vHosts requires 8 vCore and 12 Gb of RAM, while the vSwitch requires 1vCpu and 2 GB of RAM

Be careful on the ramdisk and file size in the hadoop_mem() function

```bash
bin/dmn --controller lxcremote,ip=192.168.0.1 --bastion="192.168.0.10" --workers="192.168.0.10,192.168.0.11"  --custom=/vagrant/algo_experiments/fattree/fattree_topo.py,/vagrant/algo_experiments/experiments_fattree.py  --test memory --topo ft,4,500,8,12,1,2
```

