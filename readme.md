# Neopixel over Modbus TCP

This repository aims to remotely control a set of Neopixels via a Modbus TCP server running on a RaspberryPi. It's aimed at large installations (~800 leds) with high update rates (~30 fps). This allows the processing of the data to be done on a more powerful PC and then the frames sent to the RPi over ethernet to be rendered. Future updates will eliminate the RPi and only require a basic ethernet-enabled microcontroller. Using Wifi is also possible but will drastically reduce performance.

The client side functions are designed to mimic exactly the functions of the Adafruit Circuit Python Library for Neopixels. This allows you to swap the code directly from an RPi to a PC without making changes. 

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