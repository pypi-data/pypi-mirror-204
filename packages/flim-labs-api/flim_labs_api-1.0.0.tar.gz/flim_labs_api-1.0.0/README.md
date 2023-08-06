# flim_labs_api

## What is it? 

<b>flim_labs_api</b> is a Python API developed for controlling, acquiring and displaying <b>time tagged fluorescence photons' data</b> streamed from a data acquisition card based on FPGA technology in order to perform real time <b>Fluorescence Lifetime Imaging (FLIM) and Spectroscopy applications</b>.
Overall, this API sets up a communication system between Python and a FLIM data acquisition system based on FPGA that can receive data in various modes and store it for processing.

The complete FLIM kit developed by FLIM LABS for performing Fluorescence Lifetime Spectroscopy and Imaging looks like this:

1. Fiber-coupled picosecond pulsed laser module

2. FLIM data acquisition card

3. Single-photon SPAD detector

4. FLIM studio software


## How to get drivers 

For getting the *drivers* allowing the communication with the data acquisition card email us at info@flimlabs.com. 


## How to get the API

You can install flim_labs_api with the requested dependencies with the following *pip* command:

```
pip install flim_labs_api

```


## Main features 

In the API five different acquisition modes are specified:

| Acquisition mode | Description |
|----------|----------|
| <b>Unset</b> | This is the default value of acquisition mode |
| <b<Photons_tracing</b> | Acquires the number of fluorescence photons in 100 microseconds time bins |
| <b<Spectroscopy</b> | Acquires the number of fluorescence photons in 50-100 picoseconds time bins (depending on the pulsed laser's frequency) and reconstruct the fluorescence lifetime decay curve |
| <b>Measure frequency</b> | Acquires the frequency of the laser's pulses with a precision of tens/hundreds of Hz for repetition rates of tens of MHz|
| <b>Acquire_raw_data</b>| Acquires and saves the data coming from the FPGA as binary files without processing |