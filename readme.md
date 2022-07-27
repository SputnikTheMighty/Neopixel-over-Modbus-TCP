# Neopixel over Modbus TCP

This repository aims to remotely control a set of Neopixels via a Modbus TCP server running on a RaspberryPi.

## Setup
### On Raspberry Pi
- run `start_server.py -n <number of neopixels>`

### On Client
- to test run `test_write_time.py -a <ip address of server>`

## Register Layout
One modbus register is 16 bytes. 3 bytes are needed per pixel, so 2 registers are used per pixel. The global brightness can be controlled via it's own register.

```
   ┌──────────────────┐
   │Global Brightness │
   ├──────────────────┤
   │Pixel 0 RED BLUE  │
   ├──────────────────┤
   │Pixel 0 GREEN     │
   ├──────────────────┤
   │Pixel 1 RED BLUE  │
   ├──────────────────┤
   │Pixel 1 GREEN     │
   ├──────────────────┤
   │...               │
   ├──────────────────┤
   │Pixel N RED BLUE  │
   ├──────────────────┤
   │Pixel N GREEN     │
   └──────────────────┘
```


## Setting up modbus tcp server on local host

**Linux only**  
Modbus runs on port 502. Regular user does not have access to this. You may need to redirect traffic with:

```
sudo iptables -t nat -A PREROUTING -p tcp --dport 502 -j REDIRECT --to-ports 5020
```