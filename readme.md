# Neopixel over Modbus TCP

## Register Layout

```
   ┌──────────────────┐
   │Render            │
   ├──────────────────┤
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
Modbus runs on port 502. Regular user does not have access to this. Change the port number in `start_tcp_server.py` to 5020 and  redirect traffic with:

```
sudo iptables -t nat -A PREROUTING -p tcp --dport 502 -j REDIRECT --to-ports 5020
```