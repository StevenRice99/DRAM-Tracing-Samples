#!/bin/bash
# Trace "main.py" using Intel pin.
~/pin/pin -t ~/pin/source/tools/SimpleExamples/obj-intel64/pinatrace.so -o ~/Python-Memory-Capture/trace-pin.txt -- /usr/bin/python3 ~/DRAM-Tracing-Samples/main.py