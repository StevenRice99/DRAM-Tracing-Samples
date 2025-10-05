#!/bin/bash
# Trace using Valgrind.
TEMP_FILE="${HOME}/DRAM-Tracing-Samples/temp-trace.log"
OUTPUT_FILE="${HOME}/DRAM-Tracing-Samples/trace-valgrind.txt"
TARGET_CMD="/usr/bin/python3 ${HOME}/DRAM-Tracing-Samples/main.py"
# Use getopts to parse command-line flags and their values.
while getopts 'p:t:o:s:' flag; do
  case "${flag}" in
    # -t: The temporary file path.
    t) TEMP_FILE="${OPTARG}" ;;
    # -o: The output trace file path.
    o) OUTPUT_FILE="${OPTARG}" ;;
    # -s: The target command to be traced.
    s) TARGET_CMD="${OPTARG}" ;;
    # Handle invalid options.
    *) 
      echo "Usage: $0 [-t temp_path] [-o output_path] [-s 'command_to_trace']"
      exit 1 
      ;;
  esac
done
# Remove old files if needed.
rm -f ${TEMP_FILE}
rm -f ${OUTPUT_FILE}
# Print details about the run.
echo "Running Valgrind with the following configuration:"
echo "- Temporary File: ${TEMP_FILE}"
echo "- Output File:    ${OUTPUT_FILE}"
echo "- Target Command: ${TARGET_CMD}"
start_seconds=$(date +%s)
echo "- Start Time:     $(date)"
echo "--------------------------------------------------"
# Trace memory using Valgrind.
valgrind --tool=lackey --trace-mem=yes --log-file=${TEMP_FILE} ${TARGET_CMD}
# Copy into a format DRAMSys can read.
/usr/bin/python3 ~/DRAM-Tracing-Samples/trace_valgrind.py ${TEMP_FILE} ${OUTPUT_FILE}
end_seconds=$(date +%s)
echo "- End Time:       $(date)"
elapsed_seconds=$((end_seconds - start_seconds))
echo "- Elapsed Time:   $elapsed_seconds seconds"
# Remove the temporary file.
rm -f ${TEMP_FILE}
echo "--------------------------------------------------"
echo "First 10 lines:"
head ${OUTPUT_FILE}