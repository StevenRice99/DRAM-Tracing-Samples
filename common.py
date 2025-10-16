import logging
import os
from pathlib import Path

# The home path.
HOME = os.path.expanduser("~")
# Number of lines to generate.
ENTRIES = 10000
# Megabytes to generate up to.
MEGABYTES = 4096
# Multiple megabytes to generate up to.
MEGABYTES_MULTIPLE = [2048, 4096, 8192, 16384]
# Percentage of operations which are reads.
READ = 0.9
# Multiple percentages of operations which are reads.
READ_MULTIPLE = [0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
# Output folder path.
OUTPUT_FOLDER = os.path.join(HOME, "DRAMSys", "configs", "traces", "synthetic")
# Output file path.
OUTPUT = os.path.join(OUTPUT_FOLDER, "synthetic.stl")
# Random generation seed.
SEED = 42
# Multiple random generation seeds.
SEED_MULTIPLE = [42, 43, 44, 45, 46, 47, 48, 49, 50, 51]
# The default clock speed.
CLK_MHZ = 200
# The default trace.
TRACE = "traces/example.stl"
# The default configs folder.
CONFIGS = os.path.join(HOME, "DRAMSys", "configs")
# The default executable path.
DRAM_SYS = os.path.join(HOME, "DRAMSys", "build", "bin", "DRAMSys")
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


def get_files(
        directory: str
) -> list[str]:
    """
    Get all file paths in a directory.
    :param directory: The directory.
    :type directory: str
    :return: All file paths in the directory.
    :rtype: list[str]
    """
    return [os.path.join(directory, entry.name) for entry in Path(directory).iterdir() if entry.is_file()]
