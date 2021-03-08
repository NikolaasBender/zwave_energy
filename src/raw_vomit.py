import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
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
options.set_save_log_level('Info')
options.set_logging(False)
options.lock()

#Create a network object
network = ZWaveNetwork(options, log=None)

man = network.manager

print('Auto data parser initialized')

# pass value updated
def value_updated(network, node, value):
    pass
    
dispatcher.connect(value_updated, ZWaveNetwork.SIGNAL_VALUE)


value_ids = {}

for node in network.nodes:
    print("node number:", node)
    sensor_dat = network.nodes[node].get_configs()
    for key, value in sensor_dat.items():
        print(key, value, value.value_id)
        if value.value_id in value_ids:
            value_ids[value.value_id] += 1
        else:
            value_ids[value.value_id] = 1


# log stuff


filetime = "value_ids_" + time.strftime("%Y%m%d-%H%M%S")
counter = 0


exit = False
while not exit:
    for node in network.nodes:
        print("node number:", node)
        sensor_dat = network.nodes[node].get_sensors()
        for key, value in sensor_dat.items():
            if value.value_id in value_ids:
                value_ids[value.value_id] += 1
                print(network.nodes[node].get_sensor_value(value.value_id))
            else:
                value_ids[value.value_id] = 1


    if (counter % 10) == 0:
        log = open(filetime, "w")
        log.write(json.dumps(value_ids))
        log.close()


    time.sleep(3)
    counter+=1
    
    if len(value_ids)==84:
        parse = open("file_names.csv", "a")
        parse.write(filetime + ",")
        parse.close()
        exit = True

dispatcher.disconnect(value_updated, ZWaveNetwork.SIGNAL_VALUE)