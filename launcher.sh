#!/bin/sh

export XDG_RUNTIME_DIR="/run/user/1000"

cd /home/pi/skitrock
sleep 10
python3 start.py
