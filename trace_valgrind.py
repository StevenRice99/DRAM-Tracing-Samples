import re
import sys


# A regular expression to parse the relevant lines from the Lackey log.
# It looks for lines starting with ' ', followed by L, S, or M,
# then a space, a hex address, a comma, and a number.
mem_access_pattern = re.compile(r"^[ ](L|S|M) ([0-9a-fA-F]+),(\d+)")
# Check if input and output filenames are provided.
if len(sys.argv) != 3:
    print("Usage: python3 trace_valgrind.py <input_lackey_log> <output_dramsys_trace>")
    sys.exit(1)
input_filename = sys.argv[1]
output_filename = sys.argv[2]
try:
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        num = 0
        for line in infile:
            match = mem_access_pattern.match(line)
            if match:
                op_type = match.group(1)
                address = match.group(2)
                # Convert Lackey operations to DRAMSys format.
                if op_type == 'L':
                    # Load is a Read.
                    outfile.write(f"{num}\tread\t0x{address}\n")
                elif op_type == 'S':
                    # Store is a Write.
                    outfile.write(f"{num}\twrite\t0x{address}\n")
                elif op_type == 'M':
                    # Modify is a Read followed by a Write.
                    outfile.write(f"{num}\tread\t0x{address}\n")
                    outfile.write(f"{num}\twrite\t0x{address}\n")
                num += 1
    print("Processing complete!")
except FileNotFoundError:
    print(f"Error: Input file '{input_filename}' not found.")
