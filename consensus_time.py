import time
import requests    
import argparse
from concurrent.futures import ProcessPoolExecutor
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.log import info, setLogLevel
from mininet.cli import CLI
from mininet.topo import LinearTopo
from mininet.clean import cleanup

REMOTE_CONTROLLER_IP = "192.168.56.101"
CLUSTER_NODES = {"192.168.56.101", "192.168.56.102", "192.168.56.103"}
AVG_TRIES = 1

switch_num = 0

def queryTopo(ip):
    global switch_num
    result_time = 0
    while result_time == 0:
        r = requests.get(f'http://{ip}:8181/rests/data/network-topology:network-topology/topology=flow:1', auth=('admin', 'admin'))
        result_time = time.time()
        rj = r.json()
        if "node" not in rj["network-topology:topology"][0].keys() or len(rj["network-topology:topology"][0]["node"]) < switch_num:
            result_time = 0
    return ip, result_time

def waitForTopoEmpty():
    for ip in CLUSTER_NODES:
        while True:
            r = requests.get(f'http://{ip}:8181/rests/data/network-topology:network-topology/topology=flow:1', auth=('admin', 'admin'))
            rj = r.json()
            if "node" not in rj["network-topology:topology"][0].keys() or len(rj["network-topology:topology"][0]["node"]) < switch_num:
                break

def measure():
    global switch_num
    worstResult = 0
    cleanup()
    waitForTopoEmpty()

    with ProcessPoolExecutor(max_workers=3) as executor:
        results = executor.map(queryTopo, CLUSTER_NODES)
        net = Mininet(topo=LinearTopo(k=switch_num), controller=RemoteController('c1', ip=REMOTE_CONTROLLER_IP, port=6653))
        net.start()
        start_time = time.time()
        for i, result in enumerate(results):
            diff = result[1]-start_time
            print(f"{result[0]} = {diff}")
            worstResult = max(worstResult, diff)
        print(f"SDN consensus time is {worstResult}")

    net.stop()
    return worstResult

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="measure consensus time of sdn controller")
    parser.add_argument("n", type=int, help="number of switches")
    args = parser.parse_args()
    switch_num = args.n

    #setLogLevel('info') # mininet logs
    resultSum = 0
    for i in range(AVG_TRIES) :
        print(f"######### MEASURE NUMBER {i+1}")
        resultSum += measure()
    print("")
    print(f"AVERAGE CONSENSUS TIME IS {resultSum/AVG_TRIES}")