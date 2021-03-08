import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
from openzwave.command import *
import signal
import six
if six.PY3:
    from pydispatch import dispatcher
else:
    from louie import dispatcher

from datetime import datetime

import time
import json

device="/dev/ttyACM0"
#Define some manager options
options = ZWaveOption(device, \
  config_path="../config", \
  user_path=".", cmd_line="")
options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(True)
# options.set_save_log_level(log)
options.set_save_log_level('None')
options.set_logging(False)
options.lock()

#Create a network object
network = ZWaveNetwork(options, log=None)
# node = man.addNode(homeId)
# watch = man.addWatcher(cb)
# driver = man.addDriver(device)

exit = False
man = network.manager
# node = man.addNode(homeId)
# watch = man.addWatcher(cb)
# driver = man.addDriver(device)

print('setup complete')

exit = False
def sigint_handler(signal, frame):
    global exit
    exit = True
signal.signal(signal.SIGINT, sigint_handler)

value_ids = {}

ids_file = open("useful_ids.txt", 'r')
good_ids = [int(id) for id in ids_file.readlines()]
ids_file.close()

for node in network.nodes:
    print("node number:", node)
    sensor_dat = network.nodes[node].get_configs()
    for key, value in sensor_dat.items():
        print(key, value, value.value_id)
        if value.value_id in good_ids:
            value_ids[value.label] = value.value_id


# Loop until we're told to exit:
print("Running: Ctrl+C to exit.")
counter = 0

value_data = {}
for v in good_ids:
    value_data[str(v)] = []

while not exit:
    # df.to_csv(csv)
    # openzwave.comm
    usable = 0
    for node in network.nodes:
        # print("node number:", node)
        sensor_dat = network.nodes[node].get_sensors()
        
        for key, value in sensor_dat.items():
            # sensor_dat[key]
            # print(key, value, value.value_id)
            
            if value.value_id in good_ids:
                raw_val = network.nodes[node].get_sensor_value(value.value_id)
                # if value.label not in value_ids.items():
                #     value_ids[value.label] = value.value_id
                if type(raw_val) == float:
                    value_data[str(value.value_id)].append(raw_val)               

    with open('label_id_relate.txt', 'w') as labels_file: 
        labels_file.write(json.dumps(value_ids))

    with open('id_w_data.txt', 'w') as data_file: 
        data_file.write(json.dumps(value_data))

    print("running")
    time.sleep(1)
    # signal.pause()

# dispatcher.disconnect(value_updated, ZWaveNetwork.SIGNAL_VALUE)
