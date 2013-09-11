#!/usr/bin/python

import sys

from oslo.config import cfg
import neutron.openstack.common.gettextutils as gtutil
gtutil.install('')
# from neutron.openstack.common import log as logging
import neutron.agent.linux.interface as vif_driver
from quantumclient.quantum import client as qclient
import quantumclient.common.exceptions as qcexp
from quantum.api.v2 import attributes
from neutron.agent.common import config

# LOG = logging.getLogger(__name__)

# Arg 1: controller host
# Arg 2: name of admin user
# Arg 3: admin user password
# Arg 4: tenant name
# Arg 5: uuid of VM
# Arg 6: MAC address of tap interface
# Arg 7: name of tap interface 

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

host = sys.argv[1]
user = sys.argv[2]
pw = sys.argv[3]
tenant = sys.argv[4]
vm_uuid = sys.argv[5]
mac_addr = sys.argv[6]
interface = sys.argv[7]

KEYSTONE_URL='http://' + host + ':5000/v2.0'
 
qc = qclient.Client('2.0', auth_url=KEYSTONE_URL, username=user,
tenant_name=tenant, password=pw)

prefix, net_name = interface.split('__')
port_name = net_name + '_p'
try:
    nw_id = qc.list_networks(name=net_name)['networks'][0]['id']
except qcexp.QuantumClientException as e:
    print >> sys.stderr, e
    exit(1)

p_spec = {'port': {'admin_state_up': True,
                   'name': port_name,
                   'network_id': nw_id,
                   'mac_address': mac_addr,
                   'device_id': vm_uuid,
                   'device_owner': 'compute:None'}}

try:
    port = qc.create_port(p_spec)
except qcexp.QuantumClientException as e:
    print >> sys.stderr, e
    exit(1)

port_id = port['port']['id']
br_name = 'br-ex'

conf = cfg.CONF
config.register_root_helper(conf)
conf.register_opts(vif_driver.OPTS)

driver = vif_driver.OVSInterfaceDriver(cfg.CONF)
driver.plug(nw_id, port_id, interface, mac_addr, br_name)

print br_name, port_name, port_id, net_name, nw_id
