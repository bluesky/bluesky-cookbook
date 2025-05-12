---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Flyscanning Basics

Collecting synchrotron data "on the fly" rather than point-by-point makes use of specialized equipment to dramatically improve throughput. Instead of waiting for conditions to stabilize at each point along a scan, data can be collected by taking snapshots as changes occur continuously over a wide range of interest. In order to support this capability at facility scale, DSSI has identified standard hardware and software approaches which meet the needs of multiple techniques. Broadly speaking, these flyscanning approaches include:

* Measurements and position data are collected synchronously. (time-based)
* Measurements are collected at specific pre-defined positions. (position-based)
* Measurement and position data are collected independently, using time stamps and interpolation to co-bin streams. (asynchronous)

Implementing flyscanning in a supportable manner requires standards in hardware and software. A controls and data acquisition stack which satisfies this need is summarized as follows:

* PandABox position and signal acquisition system with FMC ACQ427ELF 8 channels ADC at 16 bit / 2 MSPS​ and 4 monitor cards
* PandABox firmware​ PandABlocks-FPGA 3.0-4​ or greater
* PandABox EPICS driver PandaBlocks-ioc 0.11.5​ or greater
* Bluesky data acquisition interface layer ophyd-async 0.10.0a2​ or greater
* Bluesky 1.13.1 or later
* Tiled 0.1.0b20 or later (if used)

This implementation is described in the remaining sections of this tutorial.
