# SDNShield

![version](https://img.shields.io/badge/version-0.0-red) ![version](https://img.shields.io/badge/status-dev-red) ![version](https://img.shields.io/badge/build-passing-green) ![version](https://img.shields.io/badge/license-MIT-blue)

## Motivation

SDN(Software Defined Network) is a networking technology that enables dynamic, programmatically efficient network configuration. 

## Tech/framework used

* TShark (Expected)
* ONOS
* OpenVSwitch

## Requirements

* Python 3
* Java 11 or greater
* TShark
* ONOS 2.4.0 or greater
* OpenVSwitch with OpenFlow protocol 1.1 or greater

## Features

SDNShield detect and block DoS attack using dynamic flow rule generation of SDN. Also, SDNShield provides robustness from intelligent attack which is conducted by adjusting packet flooding interval.

## Installation

### Linux(Ubuntu)

```bash
#Install requirements on SDN switch
sudo apt install python3 openvswitch-switch 

#Install requirements on SDN controller
sudo apt install openjdk-11-jdk openjdk-11-jre python3 wget
wget https://repo1.maven.org/maven2/org/onosproject/onos-releases/2.4.0/onos-2.4.0.tar.gz
tar -xvf onos-2.4.0.tar.gz
sudo cp onos-2.4.0 /opt/onos
/opt/onos/bin/onos-service start

#Install requirements on honeypot
sudo apt install python3 tshark

#Download SDNShiled source (execute on switch/controller/honeypot)
git clone https://github.com/junhyeok-dev/JLEVA-cpp.git
```

## How to use?

Editing.