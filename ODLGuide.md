# Environment setup guide
VM setup:
mininet - download from mininet site

odl - ubuntu live server

1) Setup static ip *.101

2) install java 11(apt get) and newest maven(manually, set maven home folder in ~/.profile)

3) setup odl build
```bash
mkdir ~/.m2
wget -q -O - https://raw.githubusercontent.com/opendaylight/odlparent/master/settings.xml > ~/.m2/settings.xml
```
https://wiki-archive.opendaylight.org/view/GettingStarted:Pulling,_Hacking,_and_Pushing_All_the_Code_from_the_CLI

4) After karaf started,
In odl CLI
```bash
feature:install odl-restconf
feature:install odl-openflowplugin-flow-services-rest
feature:install odl-ovsdb-southbound-impl-ui
```

on mininet VM
```bash
sudo mn --topo tree,8 --mac --controller=remote,ip=192.168.56.101,port=6633 --switch ovsk,protocols=OpenFlow13
```

5) Get inventory out of controller using restapi GET request http://192.168.56.101:8181/rests/data/opendaylight-inventory:nodes (requires auth admin:admin)

Get topology http://192.168.56.101:8181/rests/data/network-topology:network-topology/topology=flow:1

6) Add 2 more SDN VMs by cloning

7) For each VM run
```
bin/configure_cluster.sh 1 192.168.56.101 192.168.56.102 192.168.56.103
bin/configure_cluster.sh 2 192.168.56.101 192.168.56.102 192.168.56.103
bin/configure_cluster.sh 3 192.168.56.101 192.168.56.102 192.168.56.103

feature:install odl-restconf odl-openflowplugin-flow-services-rest odl-ovsdb-southbound-impl-ui odl-mdsal-distributed-datastore odl-clustering-test-app odl-toaster
```

8) run mininet like before, request inventory out of each controller, all switches should appear

9) pingall not working by default(packets dropped), to enable:
```
sh sudo ovs-ofctl -O OpenFlow13 add-flow s1 actions=NORMAL
sh sudo ovs-ofctl -O OpenFlow13 add-flow s2 actions=NORMAL
sh sudo ovs-ofctl -O OpenFlow13 add-flow s3 actions=NORMAL
sh sudo ovs-ofctl -O OpenFlow13 add-flow s4 actions=NORMAL
sh sudo ovs-ofctl -O OpenFlow13 add-flow s5 actions=NORMAL
sh sudo ovs-ofctl -O OpenFlow13 add-flow s6 actions=NORMAL
sh sudo ovs-ofctl -O OpenFlow13 add-flow s7 actions=NORMAL
# ... for each switch(can also be added through odl restapi)
```
10) If you configure node as cluster but other nodes are not started, rest api gives you 401 unauthorized no matter what. Better start all nodes before testing.
Startup clusters sequentially, first master, then first slave, then the second one

# Some rest api examples
```
http://192.168.56.102:8181/rests/operations GET
http://192.168.56.102:8181/rests/operations/toaster:make-toast POST
{
    "input" : {
        "toasterDoneness" : 10,
        "toasterToastType" : "white-bread"
    }
}
http://192.168.56.102:8181/rests/operations/toaster:restock-toaster POST
{
  "input" :
  {
     "toaster:amountOfBreadToStock" : "3"
  }
}
http://192.168.56.102:8181/rests/data/toaster:toaster GET
{
    "toaster:toaster": {
        "toasterStatus": "up",
        "toasterModelNumber": "Model 1 - Binding Aware",
        "toasterManufacturer": "Opendaylight"
    }
}

http://192.168.56.101:8181/rests/data/opendaylight-inventory:nodes/node=openflow%3A1/flow-node-inventory:table=2/flow-node-inventory:flow=127 PUT
{
     "flow-node-inventory:flow": [
         {
             "id": "127",
             "table_id": 2,
             "installHw": false,
             "barrier": false,
             "flow-name": "FooXf3",
             "strict": false,
             "idle-timeout": 34,
             "priority": 2,
             "hard-timeout": 12,
             "cookie_mask": 255,
             "match": {
                 "ethernet-match": {
                     "ethernet-source": {
                         "address": "00:00:00:00:00:01"
                     }
                 }
             },
             "cookie": 3,
             "instructions": {
                 "instruction": [
                     {
                         "order": 0,
                         "apply-actions": {
                             "action": [
                                 {
                                     "order": 0,
                                     "drop-action": {}
                                 }
                             ]
                         }
                     }
                 ]
             }
         }
     ]
 }
 ```
https://docs.opendaylight.org/en/stable-nitrogen/user-guide/openflow-plugin-project-user-guide.html#end-to-end-flows

https://docs.opendaylight.org/projects/openflowplugin/en/latest/users/flow-examples.html

https://docs.opendaylight.org/en/stable-potassium/getting-started-guide/clustering.html

