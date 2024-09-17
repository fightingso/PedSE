#import numpy as np
import torch

class PartialIndividual:
    """
    Class for an individual in the population.

    Args:
      chrom_len: int
        Length of the chromosome.
      mutate_prob: float
        Probability
      device: torch.device
        Device on which tensors are allocated ('cpu' or 'cuda').
    """

    # Initialize the individual with a random chromosome.
    def __init__(
        self,
        chrom_len: int,
        mutate_prob: float,
        device: torch.device
    ) -> None:
        self.chrom = torch.randint(0, 2, (chrom_len,), device=device)
        self.fitness = 1e9
        self.chrom_len = chrom_len
        self.mutate_prob = mutate_prob
        

    # Perform crossover between two parents.
    def crossover(
        self,
        parent1: "PartialIndividual",
        parent2: "PartialIndividual",
        index1: int,
        index2: int,
    ) -> None:
        if index1 > index2:
            index1, index2 = index2, index1
        self.chrom[:index1] = parent1.chrom[:index1]
        self.chrom[index1:index2] = parent2.chrom[index1:index2]
        self.chrom[index2:] = parent1.chrom[index2:]
        self.mutate()

    # Mutate the chromosome.
    def mutate(self) -> None:
        for i in range(self.chrom_len):
            if  torch.rand(1).item() < self.mutate_prob:
                self.chrom[i] = 1 - self.chrom[i]


class PartialPopulation:
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
     
    """

    # Initialize the population with random individuals.
    def __init__(
        self,
        pop_size: int,
        chrom_len: int,
        mutate_prob: float,
        crossover_prob: float,
        device: torch.device
        
    ) -> None:
        self.population = [PartialIndividual(chrom_len, mutate_prob,device) for _ in range(pop_size)]
        self.crossover_prob = crossover_prob

    # Perform crossover between parents.
    def crossover(self) -> None:
        for i in range(int(len(self.population) * (1 - self.crossover_prob)), len(self.population)):
            parent1, parent2 =  torch.randint(0, len(self.population) // 4, (2,))
            index1, index2 = torch.randint(0, self.population[0].chrom_len, (2,))
            self.population[i].crossover(self.population[parent1], self.population[parent2], index1, index2)

    # Reset the fitness of the individuals.
    def reset_fitness(self) -> None:
        for individual in self.population:
            individual.fitness = 1e9
