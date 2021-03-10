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
import rospy
from zwave_energy.msg import Combined, Current, Device_power, Power
import powers 
import currents

unique_ids = []

device="/dev/ttyACM0"
#Define some manager options
options = ZWaveOption(device, \
  config_path="../config", \
  user_path=".", cmd_line="")
options.set_console_output(False)
options.set_logging(False)
options.lock()

dev_pubs = {}
good_ids = []

power_pub = rospy.Publisher(name='/energy/powers', Power)
current_pub = rospy.Publisher(name='/energy/currents', Current)

def setup(network):
    # for n in network.nodes:
    #     dev_pubs[n] = rospy.Publisher(name="/energy/full_dev_" + str(n), Device_power)
    
    for k in powers.powers_bac.keys():
        # dev = powers.powers_bac[k]["dev"]
        # clamp = powers.powers_bac[k]['clamp']
        # powers.powers_bac[k]['pub'] = rospy.Publisher(name='/energy/dev_' + str(dev) + '/clamp_' + str(clamp) + '/power')
        good_ids.append(k)

    for k in currents.currents_bac.keys():
        # dev = currents.currents_bac[k]["dev"]
        # clamp = currents.currents_bac[k]['clamp']
        # currents.currets_bac[k]['pub'] = rospy.Publisher(name='/energy/dev_' + str(dev) + '/clamp_' + str(clamp) + '/current')
        good_ids.append(k)

exit = False
def sigint_handler(signal, frame):
    global exit
    exit = True

# Connect to events
def value_updated(network, node, value):
    # data.append([value.parent_id, value.label, value.data_as_string, value.units, value.value_id])

    # if value.units == 'kWh' and value.label != "Previous Reading":
    #     kwatth.append([value.parent_id, value.data, value.value_id])
    if value.units == 'W' and value.label != "Previous Reading":
        msg = Power
        id = powers.powers_bac[value.value_id]
        dev = powers.powers_bac[id]["dev"]
        clamp = powers.powers_bac[id]['clamp']
        msg.device_id = dev
        msg.clamp_num = clamp
        msg.power = value.data
        power_pub.publish(msg)


    if value.units == 'A' and value.label != "Previous Reading":
        msg = Current
        id = currents.currets_bac[value.value_id]
        dev = currents.currets_bac[id]["dev"]
        clamp = currents.currets_bac[id]['clamp']
        msg.device_id = dev
        msg.clamp_num = clamp
        msg.current = value.data
        current_pub.publish(msg)


def main():

    rospy.init_node('zwave_energy', anonymous = True)

    # get zwave info
    network = ZWaveNetwork(options, log = None)
    man = network.manager
    setup(network)
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
