![gnuradio](https://img.shields.io/badge/GNURadio-3.10.1.1-important)
![chirpstack](https://img.shields.io/badge/ChirpStack-4.2.0-brightgreen)
![NodeRed](https://img.shields.io/badge/NodeRED-3.0.2-brightgreen)
![influxdb](https://img.shields.io/badge/InfluxDB-1.6.7-brightgreen)

# Open-Source LoRaWAN System with SDR
This repository contains the code, configuration files, and documentation for our project, where we developed an open-source LoRaWAN system using a Software-Defined Radio (SDR) communicating with traditional Commercial-Off-The-Shelf (COTS) end nodes. Using GNURadio with [gr-lora_sdr](https://github.com/tapparelj/gr-lora_sdr) LoRa transceiver, to accomplish the physical layer. This project was carried out by students at the University of Agder (UiA).

![Diagram](https://github.com/Stianje/gr-lorawan_sdr/assets/119126968/d1ad6958-8528-4efe-887d-7faff8b2579b)


### Features
- Support for various frequencies and Spreading Factors (SFs)
- Ability to handle multiple concurrent devices
- System setup, including a SDR gateway, database, and user interface configuration

### GNURadio
To set up GNURadio, follow the installation instructions provided for [gr-lora_sdr](https://github.com/tapparelj/gr-lora_sdr). In addition to the standard setup, this project employs a USB interface instead of TCP, therfore also utilized [gr-osmosdr](https://osmocom.org/projects/gr-osmosdr/wiki/GrOsmoSDR) to ensure compatibility with our hardware. The 'GNURadio' directory houses a fully installed, built upon [gr-lora_sdr](https://github.com/tapparelj/gr-lora_sdr). To use it effectively, please follow the installation instructions. The GNURadio configuration can be found within the 'apps' subdirectory, named 'lora_bladerf.grc'. A generated Python file associated with this configuration, 'lora_bladerf.py', is also available. Sync word: 0x34 for LoRaWAN, check device documentation.

- The Rx chain: This configuration is designed to receive signals at the following frequencies: 868.1MHz, 868.3MHz, and 868.5MHz, and SFs of 7 and 12. We employ the ZeroMQ library to segregate these received signals efficiently.
![gnuradirx](https://github.com/Stianje/gr-lorawan_sdr/assets/119126968/c90feecc-541e-48af-b38b-297994df49ae)

- The Tx chain: We utilize ZeroMQ to distinguish between various SFs, addressing complications associated with altering the SF variable on the modulation block during runtime. The 'complex conjugate' block is employed to transform the output signal from an upchirp to a downchirp. The 'osmocom sink' block has a variable that dynamically adjusts the frequency during runtime, ensuring transmissions occur at the correct frequency.
![gnuradiotx](https://github.com/Stianje/gr-lorawan_sdr/assets/119126968/71e3f5c3-cc5d-41a6-8654-56391ecc9ed4)

### Python code
We've utilized a straightforward Python script to establish the binding and packet formatting necessary for facilitating communication between GNURadio and the ChirpStack Gateway Bridge. This script can be accessed in the 'Python' directory.
![pythoncoderxtx](https://github.com/Stianje/gr-lorawan_sdr/assets/119126968/08520bc4-5633-46f9-9d48-03cedb101a3a)

### Node-RED
Node-RED has been employed to create an User Interface (UI) for data visualization. The JSON file detailing the flow is located within the 'NodeRED' folder.

### Acknowledgments
https://github.com/tapparelj/gr-lora_sdr

