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

device="/dev/ttyACM1"
#Define some manager options
options = ZWaveOption(device, \
  config_path="../config", \
  user_path=".", cmd_line="")
options.set_console_output(True)
options.set_logging(False)
options.lock()

exit = False
def sigint_handler(signal, frame):
    global exit
    exit = True

# Connect to events
def value_updated(network, node, value, publisher):
    node.node_id
    value.label
    value.data
    value.instance

def main():
    # initialize ros
    # DO THIS

    # get zwave info
    network = ZWaveNetwork(options, log=None)
    man = network.manager
    print('setup complete')
    netmanp = network.nodes_to_dict()

    # exiting cond
    signal.signal(signal.SIGINT, sigint_handler)

    # run dispathcer
    dispatcher.connect(value_updated, ZWaveNetwork.SIGNAL_VALUE)
    
    # this spins and spits out messages over ros
    while not exit:
        signal.pause()
    # exit and disconnect dispatcher
    dispatcher.disconnect(value_updated, ZWaveNetwork.SIGNAL_VALUE)



main()