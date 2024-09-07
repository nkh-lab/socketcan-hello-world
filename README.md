## Intro
Example project for socketCAN usage.

## Install dependencies
```
sudo apt install python3-can
```

## Check CAN interfaces
1. Using ip link Command

```
ip link show
...
4: can0: <NOARP,ECHO> mtu 16 qdisc noop state DOWN mode DEFAULT group default qlen 10
    link/can
5: can1: <NOARP,ECHO> mtu 16 qdisc noop state DOWN mode DEFAULT group default qlen 10
    link/can
```
2. Check the System's dmesg log
```
sudo dmesg | grep can
[261178.980287] peak_usb 1-3.1.1.2:1.0 can0: attached to PCAN-USB FD channel 0 (device 0xFFFFFFFF)
[261463.889381] peak_usb 1-3.1.1.1:1.0 can1: attached to PCAN-USB FD channel 0 (device 0xFFFFFFFF)
```

## Bring up the CAN interfaces

```
sudo ip link set can0 up type can bitrate 500000
sudo ip link set can1 up type can bitrate 500000
```

## Run scripts
Receiver:
```
python3 receiver.py
Listening for messages on can0...
Received message on can0: ID=0x123, Data=01020304deadbeef
^C
Reception interrupted by user.
Closed can0 interface.
```
Sender:
```
python3 sender.py
Message sent on can1: ID=0x123, Data=01020304deadbeef
Closed can1 interface.
```

## Bring down the CAN interfaces

```
sudo ip link set can0 down
sudo ip link set can1 down
```
