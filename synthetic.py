import argparse
import logging
import random


# Number of lines to generate.
ENTRIES = 1000
# Megabytes to generate up to.
MEGABYTES = 4096
# Percentage of operations which are reads.
READ = 0.9
# Output file path.
OUTPUT = "synthetic.stl"
# Random generation seed.
SEED = 42
# Logging level.
LEVEL = "INFO"


def logs(
        level: str = LEVEL
) -> None:
    """
    Configure logging.
    :param level: Logging level.
    :type level: str
    :return: Nothing.
    :rtype: None
    """
    # Configure the logging.
    level = level.upper()
    if level == "CRITICAL" or level == "FATAL":
        level = logging.CRITICAL
    elif level == "ERROR":
        level = logging.ERROR
    elif level == "WARNING" or level == "WARN":
        level = logging.WARNING
    elif level == "INFO":
        level = logging.INFO
    elif level == "DEBUG":
        level = logging.DEBUG
    else:
        level = logging.NOTSET
    logging.basicConfig(level=level, format="%(asctime)s | %(levelname)s | %(message)s")
    logging.debug(f"Logging level set to '{level}'.")
    return None


def main(
        entries: int = ENTRIES,
        megabytes: int = MEGABYTES,
        read: float = READ,
        output: str = OUTPUT,
        seed: int = SEED,
        level: str = LEVEL
) -> bool:
    """
    Perform basic synthetic generation of read and write operations.
    :param entries: Number of lines to generate.
    :type entries: int
    :param megabytes: Megabytes to generate up to.
    :type megabytes: int
    :param read: Percentage of operations which are reads.
    :type read: float
    :param output: Output file path.
    :type output: str
    :param seed: Random generation seed.
    :type seed: int
    :param level: Logging level.
    :type level: str
    :return: If the file was generated successfully.
    :rtype: bool
    """
    logs(level)
    # Ensure all values are valid.
    entries = max(entries, 1)
    megabytes = max(megabytes, 1)
    read = min(max(read, 0), 1)
    if not output.endswith(".stl"):
        logging.warning(f"Output path '{output}' did not have a '.stl' extension; appending it.")
        output = f"{output}.stl"
    logging.info(f"Entries = {entries} | Megabytes = {megabytes} | Read = {read * 100}% | Seed = {seed}")
    # Set the random seed.
    random.seed(seed)
    # Write all lines.
    try:
        with open(output, "w") as f:
            for i in range(entries):
                s = f"{i}:\t{'read' if random.random() < read else 'write'}\t{hex(random.randint(0, megabytes))}\n"
                logging.debug(s)
                f.write(s)
    except Exception as e:
        logging.error(e)
        return False
    logging.info(f"Finished generating to '{output}'.")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synthetic Memory Trace Generator")
    parser.add_argument("-e", "--entries", type=int, default=ENTRIES, help="Number of lines to generate.")
    parser.add_argument("-m", "--megabytes", type=int, default=MEGABYTES, help="Megabytes to generate up to.")
    parser.add_argument("-r", "--read", type=float, default=READ, help="Percentage of operations which are reads.")
    parser.add_argument("-o", "--output", type=str, default=OUTPUT, help="Output file path.")
    parser.add_argument("-s", "--seed", type=int, default=SEED, help="Random generation seed.")
    parser.add_argument("-l", "--level", type=str, default=LEVEL, help="Logging level.")
    args = parser.parse_args()
    main(args.entries, args.megabytes, args.read, args.output, args.seed, args.level)
