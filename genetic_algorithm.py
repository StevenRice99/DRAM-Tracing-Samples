import argparse
import logging
import os.path
import random

from common import CONFIGS, DRAM_SYS, get_files, HOME, LEVEL, logs, OUTPUT_FOLDER
from configuration import Configuration

# Load all existing mappings. You may want to limit these in some way.
ADDRESS_MAPPINGS = get_files(os.path.join(CONFIGS, "addressmapping"))
MC_CONFIGS = get_files(os.path.join(CONFIGS, "mcconfig"))
MEM_SPECS = get_files(os.path.join(CONFIGS, "memspec"))
SIM_CONFIGS = get_files(os.path.join(CONFIGS, "simconfig"))
CLK_SPEEDS = [200, 400, 800]

# All the traces we want to run.
TRACES = get_files(OUTPUT_FOLDER)

# Where to save the result to.
RESULT = os.path.join(HOME, "genetic_algorithm.txt")

# Store all run instances to avoid repeatedly running them.
HISTORY = {}

# Genetic algorithm population size.
POPULATION_SIZE = 100
# The probability of a gene mutating.
MUTATION_RATE = 0.05
# The number of top individuals to carry over to the next generation without changes.
ELITES = 5
# The number of generations to run for.
GENERATIONS = 100


class Individual:
    def __init__(
            self,
            address_mapping: str,
            mc_config: str,
            mem_spec: str,
            sim_config: str,
            clk_mhz: int
    ):
        """
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
        """
        self.address_mapping = address_mapping
        self.mc_config = mc_config
        self.mem_spec = mem_spec
        self.sim_config = sim_config
        self.clk_mhz = clk_mhz
        self.fitness = float("inf")

    def calculate_fitness(
            self,
            traces: list[str] | str,
            configs_root: str = CONFIGS,
            dram_sys: str = DRAM_SYS
    ) -> float:
        """
        Get the fitness of this member.
        :param traces: The traces.
        :type traces: list[str] | str
        :param configs_root: Where to save configuration files to.
        :type configs_root: str
        :param dram_sys: The executable path.
        :type dram_sys: str
        :return: The fitness score.
        :rtype: float
        """
        self.fitness = get_fitness(self.address_mapping, self.mc_config, self.mem_spec, self.sim_config, self.clk_mhz,
                                   traces, configs_root, dram_sys)
        return self.fitness

    @classmethod
    def create_random(cls):
        """Class method to create a new individual with a random chromosome."""
        address_mapping = random.choice(ADDRESS_MAPPINGS)
        mc_config = random.choice(MC_CONFIGS)
        mem_spec = random.choice(MEM_SPECS)
        sim_config = random.choice(SIM_CONFIGS)
        clk_mhz = random.choice(CLK_SPEEDS)
        return cls(address_mapping, mc_config, mem_spec, sim_config, clk_mhz)


def get_fitness(
        address_mapping: str,
        mc_config: str,
        mem_spec: str,
        sim_config: str,
        clk_mhz: int,
        traces: list[str] | str,
        configs_root: str = CONFIGS,
        dram_sys: str = DRAM_SYS
) -> float:
    """
    Calculate fitness of a configuration.
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
    :param traces: The traces.
    :type traces: list[str] | str
    :param configs_root: Where to save configuration files to.
    :type configs_root: str
    :param dram_sys: The executable path.
    :type dram_sys: str
    :return: The fitness score.
    :rtype: float
    """
    # See if it was cached.
    if (address_mapping in HISTORY and mc_config in HISTORY[address_mapping]
            and mem_spec in HISTORY[address_mapping][mc_config]
            and sim_config in HISTORY[address_mapping][mc_config][mem_spec]
            and clk_mhz in HISTORY[address_mapping][mc_config][mem_spec][sim_config]):
        return HISTORY[address_mapping][mc_config][mem_spec][sim_config][clk_mhz]
    # If it wasn't, get it now.
    c = Configuration(f"genetic-algorithm", address_mapping, mc_config, mem_spec, sim_config, clk_mhz)
    result, _, _ = c.run(traces, True, configs_root, dram_sys)
    # Cache it for next time.
    if address_mapping not in HISTORY:
        HISTORY[address_mapping] = {}
    if mc_config not in HISTORY[address_mapping]:
        HISTORY[address_mapping][mc_config] = {}
    if mem_spec not in HISTORY[address_mapping][mc_config]:
        HISTORY[address_mapping][mc_config][mem_spec] = {}
    HISTORY[address_mapping][mc_config][mem_spec][sim_config][clk_mhz] = result
    # Return the new result.
    return result


def selection(
        population: list[Individual]
) -> tuple[Individual, Individual]:
    """
    Selects two parent individuals from the population. This implementation uses a fitness-proportional selection where
    individuals with higher fitness have a higher chance of being selected.
    :param population: The population of members.
    :type population: list[Individual]
    :return: The two parents for crossover.
    :rtype: tuple[Individual, Individual]
    """
    # Create a weighted list based on fitness scores.
    fitness_sum = sum(individual.fitness for individual in population)
    # Handle the case where the sum of fitness is zero to avoid division errors.
    if fitness_sum == 0:
        # If all individuals have a fitness of 0, select any two at random.
        return random.sample(population, 2)
    # Select parents based on their fitness weights.
    a = random.choices(population, weights=[ind.fitness for ind in population], k=1)[0]
    b = random.choices(population, weights=[ind.fitness for ind in population], k=1)[0]
    return a, b


def crossover(
        a: Individual,
        b: Individual
) -> Individual:
    """
    Crossover two individuals.
    :param a: The first parent.
    :type a: Individual
    :param b: The second parent.
    :type b: Individual
    :return: The new member.
    :rtype: Individual
    """
    address_mapping = random.choice([a.address_mapping, b.address_mapping])
    mc_config = random.choice([a.mc_config, b.mc_config])
    mem_spec = random.choice([a.mem_spec, b.mem_spec])
    sim_config = random.choice([a.sim_config, b.sim_config])
    clk_mhz = random.choice([a.clk_mhz, b.clk_mhz])
    return Individual(address_mapping, mc_config, mem_spec, sim_config, clk_mhz)


def mutate(
        individual: Individual
) -> Individual:
    """
    Mutates an individual's chromosome.
    :param individual: The individual.
    :type individual: Individual
    :return: The new member.
    :rtype: Individual
    """
    if random.random() < MUTATION_RATE:
        address_mapping = random.choice(ADDRESS_MAPPINGS)
    else:
        address_mapping = individual.address_mapping
    if random.random() < MUTATION_RATE:
        mc_config = random.choice(MC_CONFIGS)
    else:
        mc_config = individual.mc_config
    if random.random() < MUTATION_RATE:
        mem_spec = random.choice(MEM_SPECS)
    else:
        mem_spec = individual.mem_spec
    if random.random() < MUTATION_RATE:
        sim_config = random.choice(SIM_CONFIGS)
    else:
        sim_config = individual.sim_config
    if random.random() < MUTATION_RATE:
        clk_mhz = random.choice(CLK_SPEEDS)
    else:
        clk_mhz = individual.clk_mhz
    return Individual(address_mapping, mc_config, mem_spec, sim_config, clk_mhz)


def main() -> None:
    """
    Run the genetic algorithm.
    :return: Nothing.
    :rtype: None
    """
    # Create the initial population.
    population = [Individual.create_random() for _ in range(POPULATION_SIZE)]
    for generation in range(max(GENERATIONS, 1)):
        # Get the fitness and sort with the lowest being the best.
        for member in population:
            member.calculate_fitness(TRACES)
        population.sort(key=lambda x: x.fitness)
        # Save the best.
        logging.info(f"Generation {generation + 1} of {GENERATIONS} | Fitness = {population[0].fitness}")
        # Create the next generation.
        next_generation = []
        if ELITES > 0:
            next_generation.extend(population[:ELITES])
        # Generate the rest of the new population through selection, crossover, and mutation.
        while len(next_generation) < POPULATION_SIZE:
            # Selection.
            parent1, parent2 = selection(population)
            # Crossover.
            child = crossover(parent1, parent2)
            # Mutation.
            mutated_child = mutate(child)
            next_generation.append(mutated_child)
        # Repeat.
        population = next_generation
        generation += 1
    # Save results.
    with open(RESULT, "w") as f:
        b = population[0]
        f.write(f"{b.fitness}\n{b.address_mapping}\n{b.mc_config}\n{b.mem_spec}\n{b.sim_config}\n{b.clk_mhz}")
    logging.info(f"Best results saved to '{RESULT}'.")
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DRAMSys Genetic Algorithm")
    parser.add_argument("-l", "--level", type=str, default=LEVEL, help="Logging level.")
    args = parser.parse_args()
    logs(args.level)
    main()
