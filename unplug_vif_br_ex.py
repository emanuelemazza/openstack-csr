#!/usr/bin/python

import sys

from oslo.config import cfg
import neutron.openstack.common.gettextutils as gtutil
gtutil.install('')
from neutron.openstack.common import log as logging
import neutron.agent.linux.interface as vif_driver
from quantumclient.quantum import client as qclient
import quantumclient.common.exceptions as qcexp
from quantum.api.v2 import attributes

LOG = logging.getLogger(__name__)

# Arg 1: controller host
# Arg 2: name of admin user
# Arg 3: admin user password
# Arg 4: tenant name
# Arg 5: name of interface
# Arg 6: MAC address of tap interface
# Arg 7: uuid of VM
# Arg 8: name of bridge
# Arg 9: name of port
# Arg 10: id of port  
# Arg 11: name of net
# Arg 12: id of net

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

host = sys.argv[1]
user = sys.argv[2]
pw = sys.argv[3]
tenant = sys.argv[4]
interface = sys.argv[5]
mac_addr = sys.argv[6]
vm_uuid = sys.argv[7]
port_id = sys.argv[9]
nw_id = sys.argv[12]

br_name = 'br-ex'

driver = vif_driver.OVSInterfaceDriver(cfg.CONF)
driver.unplug(interface, br_name)

KEYSTONE_URL='http://' + host + ':5000/v2.0'
 
qc = qclient.Client('2.0', auth_url=KEYSTONE_URL, username=user,
tenant_name=tenant, password=pw)

try:
   qc.delete_port(port_id)
except qcexp.QuantumClientException:
   pass
