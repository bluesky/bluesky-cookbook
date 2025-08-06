# Setup: EPICS
This section outlines how to integrate a PandABox with EPICS using the `PandABlocks-ioc` a Python-based soft IOC. The IOC dynamically generates EPICS PVs at runtime by querying the PandABox, enabling control and monitoring of its FPGA functional blocks.

## Setup the IP of PandABox
To configure the IP address of the PandABox, create a text file named `panda-config.txt` with the following content. The IP address, gateway, and DNS entries in `panda-config.txt` should be updated to reflect the desired network settings for the PandABox.

```txt 
# This file contains configuration settings. In this file network and other
# settings can be adjusted.

# If ADDRESS and NETMASK are not both specified DHCP will be used instead.
# The ADDRESS field can be set to a four part dotted IP address followed by a
# network mask specification thus:

ADDRESS = 10.68.50.131
NETMASK = 255.255.255.0

# If the ADDRESS field has been set then the GATEWAY and DNS fields should be
# set:

GATEWAY = 10.68.50.1
DNS = 10.65.2.25 10.65.2.26

# Optionally the DNS search domain can be set:
#
# DNS_SEARCH = diamond.ac.uk

# The NTP server or servers can be specified here:

NTP = time1.nsls2.bnl.gov time2.nsls2.bnl.gov time3.nsls2.bnl.gov

# The machine hostname can be specified here:

HOSTNAME = xf07bm-panda1.nsls2.bnl.local

# To skip loading any zpackages at startup, either for testing or as an
# override to recover from a faulty zpkg install:
#
# NO_ZPKG
```

If a USB drive containing the `panda-config.txt` file is plugged into the rear USB port of the PandABox during boot, the device will use the settings in that file to configure its network.

To make this configuration permanent, connect the PandABox to the **INST** network using the Ethernet port on the front panel. Then, navigate to PandA's web interface using the IP address or DNS name specified in `panda-config.txt`

From the Home page, go to **ADMIN** → **Show Network Configuration**. Verify that the displayed information matches your `panda-config.txt`, then click **REPLACE NETWORK CONFIGURATION**. Once operation complete is displayed, the default network configuration has been overwritten.

## Installation of the `PandABlocks-ioc` Packages
Both `pip` and Docker can be used to install the `PandABlocks-ioc` packages.

Using pip:

```bash
pip install pandablocks-ioc
```
Using Docker:

```bash
docker run ghcr.io/pandablocks/PandABlocks-ioc:latest
```

## Run the IOC

Following command is used to run the IOC:

```bash 
python -m pandablocks-ioc softioc <pandabox host> <pv prefix> --screens-dir=<directory to output bobfiles> --clear-bobfiles
```
Replace `<pandabox_host>` with the hostname or IP address of your PandABox, and `<pv_prefix>` with the desired prefix for your EPICS PVs. The `--screens-dir` option specifies the directory where the Phoebus `.bob` files will be generated and `--clear-bobfiles` clears old `.bob` files before generation.

Additional resources are available at the links below:
- **GitHub Repository**: [PandABlocks-ioc on GitHub](https://github.com/PandABlocks/PandABlocks-ioc)
- **Documentation**: [Official Documentation](https://pandablocks.github.io/PandABlocks-ioc)
- **PyPI Package**: [pandablocks-ioc on PyPI](https://pypi.org/project/pandablocks-ioc/)