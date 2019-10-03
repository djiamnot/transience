#!/bin/bash

recordmydesktop \
    --no-cursor \
    -x 0 -y 0 --width 1920 --height 1080 \
    --fps 30 \
    -o Transience-$(date +%F-%H-%M-%s).ogv
