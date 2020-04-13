#!/bin/bash

echo 25 > /sys/class/gpio/export
echo 22 > /sys/class/gpio/export
echo 14 > /sys/class/gpio/export
echo 15 > /sys/class/gpio/export

echo low > /sys/class/gpio/gpio25/direction
echo low > /sys/class/gpio/gpio22/direction
echo low > /sys/class/gpio/gpio14/direction
echo low > /sys/class/gpio/gpio15/direction

