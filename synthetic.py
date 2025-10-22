import argparse
import logging
import os
import random

from common import ENTRIES, LEVEL, logs, MEGABYTES, OUTPUT, OUTPUT_FOLDER, READ, SEED


def generate_synthetic(
        entries: int = ENTRIES,
        megabytes: int = MEGABYTES,
        read: float = READ,
        output: str = OUTPUT,
        seed: int = SEED
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
    :return: If the file was generated successfully.
    :rtype: bool
    """
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


def generate_synthetics(
        entries: int | list[int] = ENTRIES,
        megabytes: int | list[int] = MEGABYTES,
        read: float | list[float] = READ,
        output: str = OUTPUT_FOLDER,
        seed: int | list[int] = SEED
) -> list[str]:
    """
    Generate multiple synthetic traces.
    :param entries: Numbers of lines to generate.
    :type entries: int | list[int]
    :param megabytes: Megabytes to generate up to.
    :type megabytes: int | list[int]
    :param read: Percentages of operations which are reads.
    :type read: float | list[float]
    :param output: Output folder path.
    :type output: str
    :param seed: Random generation seeds.
    :type seed: int | list[int]
    :return: The path of the successfully generated files.
    :rtype: list[str]
    """
    if isinstance(entries, int):
        entries = [entries]
    if isinstance(megabytes, int):
        megabytes = [megabytes]
    if isinstance(read, float):
        read = [read]
    if isinstance(seed, int):
        seed = [seed]
    paths = []
    os.makedirs(output)
    for e in entries:
        for m in megabytes:
            for r in read:
                r_s = str(r).replace(".", "")
                for s in seed:
                    path = os.path.join(output, f"{e}-{m}-{r_s}-{s}.stl")
                    if generate_synthetic(e, m, r, path, s):
                        paths.append(path)
    return paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synthetic Memory Trace Generator")
    parser.add_argument("-e", "--entries", type=int, default=ENTRIES, help="Number of lines to generate.")
    parser.add_argument("-m", "--megabytes", type=int, default=MEGABYTES, help="Megabytes to generate up to.")
    parser.add_argument("-r", "--read", type=float, default=READ, help="Percentage of operations which are reads.")
    parser.add_argument("-o", "--output", type=str, default=OUTPUT, help="Output file path.")
    parser.add_argument("-s", "--seed", type=int, default=SEED, help="Random generation seed.")
    parser.add_argument("-l", "--level", type=str, default=LEVEL, help="Logging level.")
    args = parser.parse_args()
    logs(args.level)
    generate_synthetic(args.entries, args.megabytes, args.read, args.output, args.seed)
