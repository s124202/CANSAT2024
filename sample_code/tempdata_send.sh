#!/bin/bash

raspi-gpio set 4 op pn dh
python3 /home/pi/sample_code/operation_code/mode3.py
sleep 1
python3 /home/pi/sample_code/operation_code/mode0.py
vcgencmd measure_temp > /home/pi/sample_code/operation_code/ondo.txt
python3 /home/pi/sample_code/operation_code/send.py /dev/ttyS0 -f --target_address 0 --target_channel 0 < /home/pi/sample_code/operation_code/ondo.txt
sleep 2m
python3 /home/pi/sample_code/operation_code/mode2.py
sudo poweroff
