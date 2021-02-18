#!/bin/bash

echo 140 > /sys/class/gpio/export
echo 149 > /sys/class/gpio/export
echo 105 > /sys/class/gpio/export
echo 148 > /sys/class/gpio/export

echo high > /sys/class/gpio/gpio140/direction
echo high > /sys/class/gpio/gpio149/direction
echo high > /sys/class/gpio/gpio105/direction
echo high > /sys/class/gpio/gpio148/direction

echo low > /sys/class/gpio/gpio140/direction
echo low > /sys/class/gpio/gpio149/direction
echo low > /sys/class/gpio/gpio105/direction
echo low > /sys/class/gpio/gpio148/direction

