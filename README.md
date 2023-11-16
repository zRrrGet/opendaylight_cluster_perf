# ODL Cluster consensus performance measurement
Consensus algorithm perfomance measurement for latest ODL version(Potassium)

# Example
```
# 50 - number of ovs switches
mininet@mininet-vm:~/odlperf$ sudo python3 consensus_time.py 50
######### MEASURE NUMBER 1
192.168.56.101 = 5.517258405685425
192.168.56.103 = 5.526172399520874
192.168.56.102 = 5.441399812698364
SDN consensus time is 5.526172399520874

AVERAGE CONSENSUS TIME IS 5.526172399520874

```
```
mininet@mininet-vm:~/odlperf$ python3 flow_throughput.py 
192.168.56.101 diff is 4.634183645248413, write throughput is 21.578773664382812 flows/s
192.168.56.102 diff is 2.7088630199432373, write throughput is 36.91585704547565 flows/s
192.168.56.103 diff is 4.796233415603638, write throughput is 20.849694194337776 flows/s
192.168.56.101 diff is 2.333477020263672, read throughput is 42.85450387195177 flows/s
192.168.56.102 diff is 1.403611660003662, read throughput is 71.24477720549791 flows/s
192.168.56.103 diff is 2.1358823776245117, read throughput is 46.81905756964863 flows/s
```