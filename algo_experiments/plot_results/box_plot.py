import matplotlib.pyplot as plt
from pathlib import Path
import json
import matplotlib as mpl
mpl.rcParams['text.usetex'] = True
SPINE_COLOR = 'gray'
import matplotlib.patches as mpatches

ALGORITHMS = ["embeddedGreedy", "embeddedBalanced", "embeddedPartition", "maxinet", "random", "roundRobin", "switchBin"]
ALGORITHMS = ["embeddedGreedy", "maxinet", "random", "roundRobin", "switchBin"]
TICKS_NAMES = {"maxinet": "Metis",
               "switchBin": "SwitchBin",
               "roundRobin": "RoundRobin",
               "random": "Random",
               "embeddedGreedy": "GreedyP",
               "embeddedBalanced": "Kbalanced",
               "embeddedPartition": "DivideSwap"}


# PLOTS FOR THE EXPERIMENTAL PART
################################  PARAMETERS THAT YOU CAN CHANGE #####################################
# Be careful that for some combination there are no results, check the combinations tested in the paper

# Possible combinations are:

# K=4, ALGORITHMS=2nd List, PHYSICAL=gros for:
#     - merged_hadoop_box()
#     - merged_memory_no_swap_box()
#     - merged_memory_swap_box()


# K=6, ALGORITHMS=1st List, PHYSICAL=gros for:
#     - merged_bw_box()
#     - minmerged_bw_box()

# K=4, ALGORITHMS=1st List, PHYSICAL=rennes for:
#     - merged_bw_box()
#     - minmerged_bw_box()

# K=6, ALGORITHMS=2nd List, PHYSICAL=rennes for:
#     - merged_bw_box()
#     - minmerged_bw_box()


K = 4
#K = 6

#ALGORITHMS = ["embeddedGreedy", "embeddedBalanced", "embeddedPartition", "maxinet", "random", "roundRobin", "switchBin"]
ALGORITHMS = ["embeddedGreedy", "maxinet", "random", "roundRobin", "switchBin"]

PHYSICAL = "gros"
# PHYSICAL = "rennes"
######################################################################################################

PATH = Path("/vagrant/algo_experiments/results/") / PHYSICAL

def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color,linewidth=4)



def merged_bw_box():
    sub_dir="500mbps/k{}".format(K)
    basic_name = "FT_K{}_Placer_{}_Physical_{}_iperf.exp{}"

    result = []
    for algo in ALGORITHMS:
        iperf =[]
        for i in range(1,11):
            name = basic_name.format(K, algo, PHYSICAL, i)
            with open(PATH / sub_dir / name, "r") as f:
                data = json.load(f)
            iperf += [float(x.split(" ")[0]) for x in data.values()]

        result.append(iperf)

    fig, ax = plt.subplots()
    #fig.set_size_inches(6, 4)
    data = result

    ax.boxplot(data)
    plt.ylabel(r'\textbf{Throughput Mbps}', fontsize=12)
    plt.xlabel(r'\textbf{Algorithm}', fontsize=12)
    plt.grid(True)

    ax.tick_params(axis='x', rotation=60)

    plt.axhline(y=478, color='green', linestyle='-')

    ticks = [TICKS_NAMES[x] for x in ALGORITHMS]
    plt.xticks(list(range(1,len(ALGORITHMS)+2)), [f'${i}$' for i in ticks])
    plt.axis([0, len(ALGORITHMS) +1 , 0, 600])
    plt.axhline(y=478, color='green', linestyle='-')
    green_patch = mpatches.Patch(color='green', label='Expected value', linestyle="-")
    plt.legend(handles=[green_patch])
    plt.tight_layout()

    #plt.show()
    name = "{}_k{}_all.pdf".format(PHYSICAL,K)
    plt.savefig(name, dpi=100,bbox_inches='tight')


def minmerged_bw_box():
    sub_dir="500mbps/k{}".format(K)
    basic_name = "FT_K{}_Placer_{}_Physical_{}_iperf.exp{}"


    result = []
    for algo in ALGORITHMS:
        iperf =[]
        for i in range(1,11):
            name = basic_name.format(K, algo, PHYSICAL, i)
            with open(PATH /sub_dir/name, "r") as f:
                data = json.load(f)
            iperf.append(min([float(x.split(" ")[0]) for x in data.values()]))

        result.append(iperf)

    fig, ax = plt.subplots()
    #fig.set_size_inches(6, 4)
    data = result

    bx=ax.boxplot(data)
    set_box_color(bx, "blue")
    plt.ylabel(r'\textbf{Throughput [Mbps]}', fontsize=12)
    plt.xlabel(r'\textbf{Algorithm}', fontsize=12)
    plt.grid(True)

    ax.tick_params(axis='x', rotation=60)
    col="orange"
    plt.axhline(y=478, color=col, linestyle='-',linewidth=3)
    plt.tick_params(axis='both', labelsize=16)

    ticks = [TICKS_NAMES[x] for x in ALGORITHMS]
    plt.xticks(list(range(1,len(ALGORITHMS)+2)), [f'${i}$' for i in ticks])
    plt.axis([0, len(ALGORITHMS) +1 , 0, 600])
    green_patch = mpatches.Patch(color=col, label=r'Expected value', linestyle="-")
    plt.legend(handles=[green_patch], fontsize=14, ncol=2, loc="upper center")
    plt.tight_layout()
    #plt.title(r'\textbf{Network overloading (min) in Lyon cluster. vFatTree $K=4$}', fontsize=14)

    #plt.show()
    name = "{}_k{}_min.pdf".format(PHYSICAL,K)
    plt.savefig(name, dpi=100,bbox_inches='tight')


def merged_hadoop_box():
    sub_dir = "hadoop/k{}".format(K)
    basic_name = "FT_K{}_Placer_{}_Physical_{}_hadoop.exp{}"

    result = []
    all_values=[]
    for algo in ALGORITHMS:
        hadoop = []
        for i in range(1,11):
            name = basic_name.format(K, algo, PHYSICAL, i)
            with open(PATH / sub_dir / name, "r") as f:
                data = json.load(f)
            hadoop.append(min([float(x) for x in data.values()]))
            all_values.append(hadoop[-1])

        result.append(hadoop)
    fig, ax = plt.subplots()
    data = result

    bx = ax.boxplot(data)
    set_box_color(bx,"blue")
    plt.ylabel(r'\textbf{Job Completition Time [Seconds]}', fontsize=12)
    plt.xlabel(r'\textbf{Algorithm}', fontsize=12)
    plt.grid(True)
    plt.tick_params(axis='both', labelsize=16)
    ax.tick_params(axis='x', rotation=60)

    #plt.axhline(y=min(all_values), color='red', linestyle='-')

    ticks = [TICKS_NAMES[x] for x in ALGORITHMS]
    plt.xticks(list(range(1,len(ALGORITHMS)+2)), [f'${i}$' for i in ticks])
    plt.axis([0, len(ALGORITHMS) +1 , 60, 150])
    ax2 = ax.twinx()
    color = 'red'
    data2 = [None, 0, 0, 0, 0, 0]
    ax2.set_ylabel(r'\textbf{Probability to crash}', color=color,
                   fontsize=12)  # we already handled the x-label with ax1
    ax2.plot(data2, "rp",markersize=10)
    ax2.tick_params(axis='y', labelcolor=color, labelsize=16)
    ax2.axis([0, len(ALGORITHMS) + 1, 0, 1])
    plt.tight_layout()
    #plt.title(r'\textbf{CPU overloading in Gros cluster.}', fontsize=14)


    #plt.show()
    name = "{}_k{}_hadoop.pdf".format(PHYSICAL,K)
    plt.savefig(name, dpi=100,bbox_inches='tight')


def merged_memory_swap_box():
    sub_dir = "memory_swap/k{}".format(K)
    basic_name = "FT_K{}_Placer_{}_Physical_{}_memory.exp{}"

    result = []
    all_values=[]
    for algo in ALGORITHMS:
        hadoop = []
        for i in range(1,11):
            name = basic_name.format(K, algo, PHYSICAL, i)
            try:
                with open(PATH / sub_dir /name, "r") as f:
                    data = json.load(f)
            except FileNotFoundError:
                continue
            hadoop.append(min([float(x) for x in data.values()]))
            all_values.append(hadoop[-1])

        result.append(hadoop)

    fig, ax = plt.subplots()
    data = result

    bx = ax.boxplot(data)
    set_box_color(bx, "blue")
    plt.ylabel(r'\textbf{Job Completition Time [Seconds]}', fontsize=12)
    plt.xlabel(r'\textbf{Algorithm}', fontsize=12)
    plt.grid(True)
    plt.tick_params(axis='both', labelsize=16)
    ax.tick_params(axis='x', rotation=60)


    ticks = [TICKS_NAMES[x] for x in ALGORITHMS]
    plt.xticks(list(range(1,len(ALGORITHMS)+2)), [f'${i}$' for i in ticks])
    plt.axis([0, len(ALGORITHMS) +1 , 60, 150])
    ax2 = ax.twinx()
    color = 'red'
    data2 = [None, 0, 0, 0.8, 0, 0.1]
    ax2.set_ylabel(r'\textbf{Probability to crash}', color=color, fontsize=12)  # we already handled the x-label with ax1
    ax2.plot(data2, "rp",markersize=10)
    ax2.tick_params(axis='y', labelcolor=color, labelsize=16)
    ax2.axis([0, len(ALGORITHMS) +1, 0, 1])
    plt.tight_layout()
    #plt.title(r'\textbf{Memory overloading test in Gros cluster. Swap}', fontsize=14)


    #plt.show()
    name = "{}_k{}_memory_swap.pdf".format(PHYSICAL,K)
    plt.savefig(name, dpi=100,bbox_inches='tight')


def merged_memory_no_swap_box():
    sub_dir = "memory_no_swap/k{}".format(K)
    basic_name = "FT_K{}_Placer_{}_Physical_{}_memory.exp{}"

    result = []
    all_values=[]
    for algo in ALGORITHMS:
        hadoop = []
        for i in range(1,11):
            name = basic_name.format(K, algo, PHYSICAL, i)
            try:
                with open(PATH / sub_dir /name, "r") as f:
                    data = json.load(f)
            except FileNotFoundError:
                continue
            hadoop.append(min([float(x) for x in data.values()]))
            all_values.append(hadoop[-1])

        result.append(hadoop)

    fig, ax = plt.subplots()
    data = result

    bx = ax.boxplot(data)
    set_box_color(bx, "blue")
    plt.ylabel(r'\textbf{Job Completition Time [Seconds]}', fontsize=12)
    plt.xlabel(r'\textbf{Algorithm}', fontsize=12)
    plt.grid(True)
    plt.tick_params(axis='both', labelsize=16)
    ax.tick_params(axis='x', rotation=60)

    #plt.axhline(y=min(all_values), color='red', linestyle='-')

    ticks = [TICKS_NAMES[x] for x in ALGORITHMS]
    plt.xticks(list(range(1,len(ALGORITHMS)+2)), [f'${i}$' for i in ticks])
    plt.axis([0, len(ALGORITHMS) +1 , 60, 150])
    ax2 = ax.twinx()
    color = 'red'
    data2 = [None,0,1,1,0,1]
    ax2.set_ylabel(r'\textbf{Probability to crash}', color=color, fontsize=12)  # we already handled the x-label with ax1
    ax2.plot(data2, "rp",markersize=10)
    ax2.tick_params(axis='y', labelcolor=color, labelsize=16)
    ax2.axis([0, len(ALGORITHMS) +1, 0, 1])

    plt.tight_layout()
    #plt.title(r'\textbf{Memory overloading test in Gros cluster. No Swap}', fontsize=14)

    name = "{}_k{}_memory_no_swap.pdf".format(PHYSICAL, K)
    plt.savefig(name, dpi=100,bbox_inches='tight')



if __name__ == '__main__':
    #merged_bw_box()
    #minmerged_bw_box()
    merged_hadoop_box()
    merged_memory_no_swap_box()
    merged_memory_swap_box()
