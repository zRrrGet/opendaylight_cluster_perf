import time
import requests
import argparse
import json

CLUSTER_NODES = ["192.168.56.101", "192.168.56.102", "192.168.56.103"]

flow = json.loads("""{
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
 }""")

for i in range(len(CLUSTER_NODES)):
    # cleanup first
    for j in range(100+100*i, 200+100*i):
        url = f'http://{CLUSTER_NODES[i]}:8181/rests/data/opendaylight-inventory:nodes/node=openflow:1/flow-node-inventory:table=2/flow-node-inventory:flow={j}'
        x = requests.delete(url, auth=('admin', 'admin'))
        if x.status_code != 204 and x.status_code != 409:
            print(f"strange status for DELETE {x.status_code}")

for i in range(len(CLUSTER_NODES)):
    start = time.time()
    for j in range(100+100*i, 200+100*i):
        url = f'http://{CLUSTER_NODES[i]}:8181/rests/data/opendaylight-inventory:nodes/node=openflow:1/flow-node-inventory:table=2/flow-node-inventory:flow={j}'
        flow["flow-node-inventory:flow"][0]["id"] = j
        x = requests.put(url, json=flow, auth=('admin', 'admin'))
        if x.status_code != 201:
            print(f"strange status for PUT {x.status_code}")
    end = time.time()

    print(f"{CLUSTER_NODES[i]} diff is {end-start}, write throughput is {100/(end-start)} flows/s")

for i in range(len(CLUSTER_NODES)):
    start = time.time()
    for j in range(100+100*i, 200+100*i):
        url = f'http://{CLUSTER_NODES[i]}:8181/rests/data/opendaylight-inventory:nodes/node=openflow:1/flow-node-inventory:table=2/flow-node-inventory:flow={j}'
        x = requests.get(url, auth=('admin', 'admin'))
        if x.status_code != 200:
            print(f"strange status for GET {x.status_code}")
    end = time.time()

    print(f"{CLUSTER_NODES[i]} diff is {end-start}, read throughput is {100/(end-start)} flows/s")
