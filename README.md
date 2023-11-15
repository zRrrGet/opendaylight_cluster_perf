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
192.168.56.101 diff is 5.341362476348877, throughput is 18.72181497563439 flows/s
192.168.56.102 diff is 3.1285452842712402, throughput is 31.96373742862216 flows/s
192.168.56.103 diff is 5.171907186508179, throughput is 19.335227101690347 flows/s
```