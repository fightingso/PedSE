import numpy as np


class Individual:
  '''
  Class for an individual in the population.

  Args:
    chrom_len: int
      Length of the chromosome.
    mutate_prob: float
      Probability
  '''

  # Initialize the individual with a random chromosome.
  def __init__(
    self,
    chrom_len: int,
    mutate_prob: float,
  ) -> None:
    self.chrom = np.random.randint(0, 2, chrom_len)
    self.fitness = 1e9
    self.chrom_len = chrom_len
    self.mutate_prob = mutate_prob

  # Perform crossover between two parents.
  def crossover(
    self,
    parent1: Individual,
    parent2: Individual,
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
      if np.random.rand() < self.mutate_prob:
        self.chrom[i] = 1 - self.chrom[i]


class Population:
  '''
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
  '''

  # Initialize the population with random individuals.
  def __init__(
    self,
    pop_size: int,
    chrom_len: int,
    mutate_prob: float,
    crossover_prob: float,
  ) -> None:
    self.population = [Individual(chrom_len, mutate_prob) for _ in range(pop_size)]
    self.crossover_prob = crossover_prob

  # Perform crossover between parents.
  def crossover(self) -> None:
    for i in range(int(len(self.population) * (1 - self.crossover_prob)), len(self.population)):
      parent1, parent2 = np.random.choice(len(self.population) // 4, size=2)
      index1, index2 = np.random.randint(0, self.population[0].chrom_len, size=2)
      self.population[i].crossover(self.population[parent1], self.population[parent2], index1, index2)

  # Reset the fitness of the individuals.
  def reset_fitness(self) -> None:
    for individual in self.population:
      individual.fitness = 1e9
