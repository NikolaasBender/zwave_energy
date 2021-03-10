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

data = []
watts = []
kwatth = []
current = []

# energy consumption mode
man.setConfigParam(0xe3a501b8, 3, 2, 2)
man.setConfigParam(0xe3a501b8, 4, 2, 2)

# disable selective reporting
man.setConfigParam(0xe3a501b8, 3, 3, 2)
man.setConfigParam(0xe3a501b8, 4, 3, 2)


# Connect to events
def value_updated(network, node, value):
    data.append([value.parent_id, value.label, value.data_as_string, value.units, value.value_id])

    if value.units == 'kWh' and value.label != "Previous Reading":
        kwatth.append([value.parent_id, value.data, value.value_id])
    if value.units == 'W' and value.label != "Previous Reading":
        watts.append([value.parent_id, value.data, value.value_id])
        
    if value.units == 'A' and value.label != "Previous Reading":
        current.append([value.parent_id, value.data, value.value_id])
        print(value.parent_id, value.label, value.data, value.units, value.value_id) 
    
    
    pass
    
dispatcher.connect(value_updated, ZWaveNetwork.SIGNAL_VALUE)


dispatcher.connect(value_updated, openzwave.network)

time.sleep(2)

value_ids = {}
print(network.nodes)


# for node in network.nodes:
#     print("node number:", node)
#     sensor_dat = network.nodes[node].get_configs()
#     print(sensor_dat)
    # for key, value in sensor_dat.items():
    #     print(sensor_dat[key])
    #     print(key, value, value.value_id)
    #     if value.value_id in value_ids:
    #         value_ids[value.value_id] = []
    #     else:
    #         value_ids[value.value_id] = []
      

# Loop until we're told to exit:
print("Running: Ctrl+C to exit.")
counter = 0

interesting_ids = []

while not exit:
    # df.to_csv(csv)
    # openzwave.comm
    # usable = 0
    # # print(network.nodes)

    # for node in network.nodes:
    #     print("node number:", node)
    #     sensor_dat = network.nodes[node].get_sensors()
        
    #     for key, value in sensor_dat.items():
    #         # sensor_dat[key]
    #         # print(key, value, value.value_id)
            
    #         if value.value_id in value_ids:
    #             # raw_val = network.nodes[node].get_sensor_value(value.value_id)
    #             # try indicies 5, 6, 7
    #             raw_val = network.nodes[node].get_values()
    #             # raw_val = network.nodes[node].get_values(class_id=0x32) # get all kinds of raw data

    #             # raw_val = network.nodes[node].get_values(label="Wattage Threshold C2")
    #             raw_val = list(raw_val.values())
    #             for o in raw_val:
    #                 print(o)
    #             if type(raw_val) == float:
    #                 useful = all(abs(x) >= 0.1 for x in value_ids[value.value_id])
    #                 if useful:
    #                     usable += 1
    #                     # print(value_ids[value.value_id])
    #                     # print(value.value_id, " is interesting")
    #                 if len(value_ids[value.value_id]) > 0:
    #                     if useful and (abs(raw_val) <= 0.98 * abs(value_ids[value.value_id][-1]) or abs(raw_val) >= 1.02 * abs(value_ids[value.value_id][-1])):
    #                         print("potentially interesting id ", value.value_id)
    #                         if value.value_id not in interesting_ids:
    #                             interesting_ids.append(value.value_id)
    #                             f = open("demofile2.txt", "w")
    #                             for e in interesting_ids:
    #                                 f.write(str(e))
    #                                 f.write('\n')
    #                             f.close()
    #                 value_ids[value.value_id].append(raw_val)
    #             # print(raw_val)
               
    #         else:
    #             value_ids[value.value_id] = []
    # # print("usable", usable)

    # print("unique vals", len(value_ids))

    # print("running")
    # time.sleep(1)
    signal.pause()

dispatcher.disconnect(value_updated, ZWaveNetwork.SIGNAL_VALUE)
