import re
import sys


# A regular expression to parse the relevant lines from the Intel Pin trace file.
# It is designed to capture the operation type (R or W) and the memory address
# from lines that represent memory accesses.
mem_access_pattern = re.compile(r"^0x[0-9a-fA-F]+:\s+(R|W)\s+0x([0-9a-fA-F]+)")
# Check if the correct number of command-line arguments (input and output files) is provided.
if len(sys.argv) != 3:
    print("Usage: python3 trace_pin.py <input_pin_trace> <output_dramsys_trace>")
    sys.exit(1)
input_filename = sys.argv[1]
output_filename = sys.argv[2]
try:
    # Open the input and output files.
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        num = 0
        for line in infile:
            # Ignore comment lines, which typically start with '#' in pinatraces.
            if line.strip().startswith('#'):
                continue
            # Attempt to match the memory access pattern in the current line.
            match = mem_access_pattern.match(line)
            if match:
                op_type = match.group(1)
                address = match.group(2)
                # The operation type from Pin ('R' or 'W') directly maps to the
                # required DRAMSys format. We write the formatted address and
                # operation to the output file.
                if op_type == 'R':
                    # Read operation.
                    outfile.write(f"{num}:\tread\t0x{address}\n")
                elif op_type == 'W':
                    # Write operation.
                    outfile.write(f"{num}:\twrite\t0x{address}\n")
                num += 1
except FileNotFoundError:
    print(f"Error: Input file '{input_filename}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")
