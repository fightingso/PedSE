
import torch
from .ppop import PartialPopulation
import random

class WholeIndividual:
    """
    Class for an individual in the population.

    Args:
      chrom_len: int
        Length of the chromosome.
      mutate_prob: float
        Probability
      ppop: PartialPopulation
        Population object
      device: torch.device
        Device on which tensors are allocated ('cpu' or 'cuda').
    """

    # Initialize the individual with a random chromosome.
    def __init__(
        self,
        chrom_len: int,
        mutate_prob: float,
        ppop: PartialPopulation,
        device: torch.device
        ) -> None:
        self.chrom =  [random.choice(ppop.population) for _ in range(chrom_len)]
        self.chrom_len = chrom_len
        self.mutate_prob = mutate_prob
        self.fitness = 1e9
        


    # Perform crossover between two parents.
    def crossover(
        self, parent1: "WholeIndividual", parent2: "WholeIndividual", index1: int, index2: int, ppop: PartialPopulation
    ) -> None:
        if index1 > index2:
            index1, index2 = index2, index1
        self.chrom[:index1] = parent1.chrom[:index1]
        self.chrom[index1:index2] = parent2.chrom[index1:index2]
        self.chrom[index2:] = parent1.chrom[index2:]
        self.mutate(ppop)

    # Mutate the chromosome.
    def mutate(self, ppop: PartialPopulation) -> None:
        for i in range(self.chrom_len):
            if torch.rand(1).item()  < self.mutate_prob:
                self.chrom[i] = random.choice(ppop.population)


class WholePopulation:
    """
    Class for the population.

    Args:
      pop_size: int
        Size of the population.
      chrom_len: int
        Length of the chromosome.
      mutate_prob: float
        Probability of mutation.
      crossover_prob: float
        Probability
      ppop: PartialPopulation
        Population object
    """

    # Initialize the population with random individuals.
    def __init__(
        self, 
        pop_size: int, 
        chrom_len: int, 
        mutate_prob: float, 
        crossover_prob: float, 
        ppop: PartialPopulation,
        device: torch.device
    ) -> None:
        self.population = [WholeIndividual(chrom_len, mutate_prob,ppop,device) for _ in range(pop_size)]
        self.chrom_len = chrom_len
        self.pop_size = pop_size
        self.crossover_prob = crossover_prob

    # Perform crossover between parents.
    def crossover(self, ppop: PartialPopulation) -> None:
        for i in range(int(len(self.population) * (1 - self.crossover_prob)), len(self.population)):
            parent1, parent2 = torch.randint(0, self.pop_size // 4, (2,))
            index1, index2 = torch.randint(0, self.chrom_len, (2,))
            self.population[i].crossover(self.population[parent1], self.population[parent2], index1, index2, ppop)

    # Reset the fitness of the individuals.
    def reset_fitness(self) -> None:
        for individual in self.population:
            individual.fitness = 1e9
