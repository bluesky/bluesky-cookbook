# Setup: Firmware

The PandABox firmware consists of a root filesystem (rootfs) and PandA packages (zpkg files). The rootfs is used to boot Linux on the Zynq module that is the heart of a PandABox, while the PandA packages are used for managing all application software.
In this implementation, the ACQ427ELF FMC module is used, configured for 8 analog input channels, as well as 4 monitor encoder cards. Given the hardware, the corresponding firmware packages are installed:
- Root filesystem:
  - boot＠PandABox-X.X.zip
- PandA packages:
  - panda-fpga＠PandABox-fmc_acq427-X.X.zpg
  - panda-server＠zynq-X.X.zpg
  - panda-slowfpga＠X.X.zpg
  - panda-webcontrol＠X.X.zpg
  - panda-webcontrol-no-subnet-validation＠X.X.zpg

“X.X” represents the version number, which is recommended to be 3.0 or greater.
The source for official releases of the PandABox root filesystem files and firmware packages is the PandABlocks GitHub page: [PandABlocks Releases](https://github.com/PandABlocks/PandABlocks.github.io/releases). 


Other configurations, outside of the standards, are possible, for applications such as using EVR (while using the FMC), PTP (while using the FMC), a higher resolution ADC (ACQ430), or not using an FMC. There are specific rootfs files for the FMC + EVR or PTP applications that need to be installed, in addition to installing the corresponding packages: 
- FPGA Firmware:
  - ***No FMC***: panda-fpga＠PandABox-no-fmc-X.X.zpg
  - ***ACQ427***: panda-fpga＠PandABox-fmc_acq427-X.X.zpg
  - ***ACQ430***: panda-fpga＠PandABox-fmc_acq430-X.X.zpg
  - ***EVR+ACQ427***: panda-fpga＠PandABox-fmc_acq427_dls_eventr-3.0-4-g6e5f0a2-dirty.zpg
  - ***PTP+ACQ427***: panda-fpga＠PandABox-fmc_acq427_ptp-3.0-4-g6e5f0a2-dirty.zpg
- TCP Server:
  - ***Standard***: panda-server＠zynq-X.X.zpg
  - ***EVR+ACQ427***: panda-server＠zynq-3.0-11-g6422090.zpg
  - ***PTP+ACQ427***: panda-server＠zynq_ptp-3.0-11-g6422090.zpg
- Others:
  - panda-slowfpga＠X.X.zpg
  - panda-webcontrol＠X.X.zpg
  - panda-webcontrol-no-subnet-validation＠X.X.zpg

The latest versions used by DSSI are stored on the DSSI SharePoint: [DSSI PandABox Firmware](https://brookhavenlab.sharepoint.com/sites/NSLS2DSSI/Shared%20Documents/Forms/AllItems.aspx?ga=1&id=%2Fsites%2FNSLS2DSSI%2FShared%20Documents%2FHardware%2FPandABox%2FFirmware&viewid=4ce5067d%2D9e28%2D4d34%2D9650%2Deed2cd454ac0).
