#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#    Adopted by Alexander Daichendt to support LXC instead of libvirt, 2023
import os
import xml.etree.ElementTree as ET

import lxc
import pyghmi.ipmi.bmc as bmc

from virtualbmc import exception
from virtualbmc import log
from virtualbmc import utils

LOG = log.get_logger()

# Power states
POWEROFF = 0
POWERON = 1

# From the IPMI - Intelligent Platform Management Interface Specification
# Second Generation v2.0 Document Revision 1.1 October 1, 2013
# https://www.intel.com/content/dam/www/public/us/en/documents/product-briefs/ipmi-second-gen-interface-spec-v2-rev1-1.pdf
#
# Command failed and can be retried
IPMI_COMMAND_NODE_BUSY = 0xC0
# Invalid data field in request
IPMI_INVALID_DATA = 0xcc

# Boot device maps
GET_BOOT_DEVICES_MAP = {
    'network': 4,
    'hd': 8,
    'cdrom': 0x14,
}

SET_BOOT_DEVICES_MAP = {
    'network': 'network',
    'hd': 'hd',
    'optical': 'cdrom',
}


class VirtualBMC(bmc.Bmc):

    def __init__(self, username, password, port, address, domain_name, **kwargs):
        super(VirtualBMC, self).__init__({username: password},
                                         port=port, address=address)
        self.domain_name = domain_name

    def get_boot_device(self):
        LOG.debug('Get boot device called for %(domain)s',
                  {'domain': self.domain_name})
        LOG.debug("Not implemented for containers")
        return IPMI_COMMAND_NODE_BUSY

    def _remove_boot_elements(self, parent_element):
        for boot_element in parent_element.findall('boot'):
            parent_element.remove(boot_element)

    def set_boot_device(self, bootdevice):
        LOG.debug('Set boot device called for %(domain)s with boot '
                  'device "%(bootdev)s"', {'domain': self.domain_name,
                                           'bootdev': bootdevice})
        LOG.debug("Not supported for containers")
        return IPMI_COMMAND_NODE_BUSY


    def get_power_state(self):
        LOG.debug('Get power state called for domain %(domain)s',
                  {'domain': self.domain_name})
        target = self.domain_name
        container = lxc.Container(target)
        if container.defined:
            if container.state == "STOPPED":
                return POWEROFF
            if container.state == "RUNNING":
                return POWERON
            return POWEROFF
        else:
            msg = ('Error getting the power state of domain %(domain)s. '
                   'Error: %(error)s' % {'domain': self.domain_name,
                                         'error': "Container undefined"})
            LOG.error(msg)
            raise exception.VirtualBMCError(message=msg)

    def pulse_diag(self):
        LOG.debug('Power diag called for domain %(domain)s',
                  {'domain': self.domain_name})
        LOG.debug("Currently not supported for containers")
        return IPMI_COMMAND_NODE_BUSY

    def power_off(self):
        LOG.debug('Power off called for domain %(domain)s',
                  {'domain': self.domain_name})
        target = self.domain_name
        container = lxc.Container(target)
        if container.defined:
            if container.running:
                container.stop()
        else:
            LOG.error('Error powering off the domain %(domain)s. '
                      'Error: %(error)s', {'domain': self.domain_name,
                                           'error': "Container not defined"})
            # Command not supported in present state
            return IPMI_COMMAND_NODE_BUSY

    def power_on(self):
        LOG.debug('Power on called for domain %(domain)s',
                  {'domain': self.domain_name})
        target = self.domain_name
        container = lxc.Container(target)
        if container.defined:
            if not container.running:
                container.start()
        else:
            LOG.error('Error powering on the domain %(domain)s. '
                      'Error: %(error)s', {'domain': self.domain_name,
                                           'error': "Container not defined"})
            # Command failed, but let client retry
            return IPMI_COMMAND_NODE_BUSY

    def power_shutdown(self):
        LOG.debug('Soft power off called for domain %(domain)s',
                  {'domain': self.domain_name})
        target = self.domain_name
        container = lxc.Container(target)
        if container.defined:
            if container.running:
                container.stop()
        else:
            LOG.error('Error soft powering off the domain %(domain)s. '
                      'Error: %(error)s', {'domain': self.domain_name,
                                           'error': "Container not defined"})
            # Command not supported in present state
            return IPMI_COMMAND_NODE_BUSY

    def power_reset(self):
        LOG.debug('Power reset called for domain %(domain)s',
                  {'domain': self.domain_name})
        target = self.domain_name
        container = lxc.Container(target)
        if container.defined:
            os.system(f"lxc-stop --kill {target}")
        else:
            LOG.error('Error resetting the domain %(domain)s. '
                      'Error: %(error)s', {'domain': self.domain_name,
                                           'error': "Container not defined"})
            # Command not supported in present state
            return IPMI_COMMAND_NODE_BUSY

