#!/bin/bash
# Trace using Intel pin.
# Default paths.
PIN_EXE="${HOME}/pin/pin"
PIN_TOOL="${HOME}/pin/source/tools/SimpleExamples/obj-intel64/pinatrace.so"
OUTPUT_FILE="${HOME}/DRAM-Tracing-Samples/trace-pin.txt"
TARGET_CMD="/usr/bin/python3 ${HOME}/DRAM-Tracing-Samples/main.py"
# Use getopts to parse command-line flags and their values.
while getopts 'p:t:o:s:' flag; do
  case "${flag}" in
    # -p: The "pin" executable.
    p) PIN_EXE="${OPTARG}" ;;
    # -t: The pin tracer program executable.
    t) PIN_TOOL="${OPTARG}" ;;
    # -o: The output trace file path.
    o) OUTPUT_FILE="${OPTARG}" ;;
    # -s: The target command to be traced.
    s) TARGET_CMD="${OPTARG}" ;;
    # Handle invalid options.
    *) 
      echo "Usage: $0 [-p pin_path] [-t tool_path] [-o output_path] [-s 'command_to_trace']"
      exit 1 
      ;;
  esac
done
# Remove the old trace file if needed.
rm -f ${OUTPUT_FILE}
# Print details about the run.
echo "Running Intel Pin with the following configuration:"
echo "- Pin Executable: ${PIN_EXE}"
echo "- Pin Tool:       ${PIN_TOOL}"
echo "- Output File:    ${OUTPUT_FILE}"
echo "- Target Command: ${TARGET_CMD}"
start_seconds=$(date +%s)
echo "- Start Time:     $(date)"
echo "---------------------------------------------------"
# Execute the final command.
# TARGET_CMD is intentionally not quoted to allow the shell to correctly.
${PIN_EXE} -t ${PIN_TOOL} -o ${OUTPUT_FILE} -- ${TARGET_CMD}
end_seconds=$(date +%s)
echo "- End Time:       $(date)"
elapsed_seconds=$((end_seconds - start_seconds))
echo "- Elapsed Time:   $elapsed_seconds seconds"
echo "---------------------------------------------------"
echo "First 10 lines:"
head ${OUTPUT_FILE}