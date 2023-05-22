==========
VirtualBMC-lxc
==========

IMPORTANT - NOTES FOR THIS FORK
-------------------------------

This project is a fork of virtualbmc (https://github.com/openstack/virtualbmc ) and allows to control LXC containers
with IPMI. The dependencies on `libvirt` have been removed and replaced with calls to the python library
`python3-lxc`, which interfaces with the userspace tools of LXC.

Requirement:

.. code-block:: bash

  apt install python3-lxc

Author Information to all files will be added after Double Blind Submission, to hold the double blind submission requirements.

Team and repository tags
------------------------

.. image:: https://governance.openstack.org/tc/badges/virtualbmc.svg
    :target: https://governance.openstack.org/tc/reference/tags/index.html

Overview
--------

A virtual BMC for controlling virtual machines using IPMI commands.

Installation
~~~~~~~~~~~~

.. code-block:: bash

  pip install virtualbmc


Supported IPMI commands
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

  # Power the virtual machine on, off, graceful off, NMI and reset
  ipmitool -I lanplus -U admin -P password -H 127.0.0.1 power on|off|soft|diag|reset

  # Check the power status
  ipmitool -I lanplus -U admin -P password -H 127.0.0.1 power status

  # Set the boot device to network, hd or cdrom
  ipmitool -I lanplus -U admin -P password -H 127.0.0.1 chassis bootdev pxe|disk|cdrom

  # Get the current boot device
  ipmitool -I lanplus -U admin -P password -H 127.0.0.1 chassis bootparam get 5

Project resources
~~~~~~~~~~~~~~~~~

* Documentation: https://docs.openstack.org/virtualbmc/latest
* Source: https://opendev.org/openstack/virtualbmc
* Bugs: https://storyboard.openstack.org/#!/project/openstack/virtualbmc
* Release Notes: https://docs.openstack.org/releasenotes/virtualbmc/

Project status, bugs, and requests for feature enhancements (RFEs) are tracked
in StoryBoard:
https://storyboard.openstack.org/#!/project/openstack/virtualbmc

For information on how to contribute to VirtualBMC, see
https://docs.openstack.org/virtualbmc/latest/contributor

