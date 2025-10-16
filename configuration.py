import json
import logging
import os.path
import re
import subprocess

from common import CLK_MHZ, CONFIGS, DRAM_SYS, TRACE


class Configuration:
    def __init__(
            self,
            simulation_id: str,
            address_mapping: str,
            mc_config: str,
            mem_spec: str,
            sim_config: str,
            clk_mhz: int = CLK_MHZ,
            trace: str = TRACE
    ):
        """
        Create a configuration.
        :param simulation_id: The name of the file for this and the run ID.
        :type simulation_id: str
        :param address_mapping: The address mapping.
        :type address_mapping: str
        :param mc_config: The MC configuration.
        :type mc_config: str
        :param mem_spec: The memory specification.
        :type mem_spec: str
        :param sim_config: The sim configuration.
        :type sim_config: str
        :param clk_mhz: The clock speed.
        :type clk_mhz: int
        :param trace: The trace.
        :type trace: str
        """
        self.simulation_id = simulation_id
        self.address_mapping = address_mapping
        self.mc_config = mc_config
        self.mem_spec = mem_spec
        self.sim_config = sim_config
        self.clk_mhz = clk_mhz
        self.trace = trace
        self.data = {
            "simulation": {
                "addressmapping": address_mapping,
                "mcconfig": mc_config,
                "memspec": mem_spec,
                "simconfig": sim_config,
                "simulationid": simulation_id,
                "tracesetup": [
                    {
                        "type": "player",
                        "clkMhz": clk_mhz,
                        "name": trace
                    }
                ]
            }
        }
        logging.debug(f"Created configuration: {self}")

    def __str__(self) -> str:
        """
        Get a detailed string of this.
        :return: All details in a string.
        :rtype: str
        """
        return f"{self.data}"

    def identifier(self) -> str:
        """
        Get a unique identifier based on the current config which can be used to help cache unique results.
        :return: The unique identifier.
        :rtype: str
        """
        return f"{self.address_mapping}-{self.mc_config}-{self.mem_spec}-{self.sim_config}-{self.clk_mhz}"

    def run(
            self,
            traces: str | list[str],
            cleanup: bool = True,
            configs_root: str = CONFIGS,
            dram_sys: str = DRAM_SYS
    ) -> tuple[float, int, dict[str, float]]:
        """
        Run this configuration against multiple traces.
        :param traces: The traces to run against.
        :type traces: str | list[str]
        :param cleanup: If we want to delete the configurations after we run them.
        :type cleanup: bool
        :param configs_root: Where to save configuration files to.
        :type configs_root: str
        :param dram_sys: The executable path.
        :type dram_sys: str
        :return: The average run time, the number of runs which were successful, and lastly the details of each run.
        :rtype: tuple[float, int, dict[str, float]]
        """
        # If only one trace was passed, convert it to a loop so it functions properly.
        if isinstance(traces, str):
            traces = [traces]
        # Initialize variables.
        results = {}
        successful = []
        count = 0
        # Loop through every trace that was requested to run.
        for trace in traces:
            # Set values for this instance.
            instance_id = f"{self.simulation_id}-{os.path.basename(trace)}"
            self.data["simulation"]["simulationid"] = instance_id
            self.data["simulation"]["tracesetup"][0]["name"] = trace
            # Write the file so it can be run with DRAMSys.
            path = os.path.join(configs_root, f"{instance_id}.json")
            with open(path, "w") as f:
                json.dump(self.data, f, indent=4)
            # Run with DRAMSys and extract the results.
            try:
                result = subprocess.run(
                    [dram_sys, path],
                    # Capture stdout and stderr.
                    capture_output=True,
                    # Decode stdout/stderr as text (UTF-8).
                    text=True,
                    # Raise an exception if the command fails (returns a non-zero exit code).
                    check=True
                )
                # Nothing to do if errors happened.
                if result.stderr:
                    logging.error(f"Error executing '{dram_sys}' with '{path}': {result.stderr}")
                    results[instance_id] = float("inf")
                # Otherwise, try to extract the execution time.
                else:
                    match = re.search(r"(\d+)\s*ps", result.stdout)
                    if match:
                        ps = int(match.group(1))
                        successful.append(ps)
                        results[instance_id] = ps
                        count += 1
                    else:
                        logging.error(f"Failed to extract the execution time from '{dram_sys}' with '{path}'.")
                        results[instance_id] = float("inf")
            except Exception as e:
                logging.error(f"Failed to execute '{dram_sys}' with '{path}': {e}")
                results[instance_id] = float("inf")
            # Remove the file if we should.
            if cleanup:
                os.remove(path)
        # Restore original values.
        self.data["simulation"]["simulationid"] = self.simulation_id
        self.data["simulation"]["tracesetup"][0]["name"] = self.trace
        return (float("inf") if count < 1 else float(sum(successful)) / count), count, results
