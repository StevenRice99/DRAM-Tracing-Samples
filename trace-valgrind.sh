#!/bin/bash
# Run Valgrind the trace "main.py" to "trace.log".
valgrind --tool=lackey --trace-mem=yes --log-file="trace.log" python3 main.py
# Copy to "trace.log" into "dramsys_trace.txt" in a format DRAMSys can read.
python3 trace_valgrind.py trace.log trace-valgrind.txt
# Remove the original.
rm trace.log