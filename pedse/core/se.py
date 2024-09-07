import numpy as np

from .ppop import PartialPopulation
from .wpop import WholePopulation


class SymbioticEvolution:
    """
    Symbiotic Evolution class that manages the co-evolution of a partial and whole population.

    Args:
      eval: function
        Function to evaluate the fitness of the population.
      chrom_len: int
        Length of the chromosome for individuals in the whole population.
      partial_pop: PartialPopulation
        A partial population object.
      whole_pop: WholePopulation
        A whole population object.
    """

    def __init__(self, eval, chrom_len: int, partial_pop: PartialPopulation, whole_pop: WholePopulation):
        self.eval = eval
        self.chrom_len = chrom_len
        self.partial_pop = partial_pop
        self.whole_pop = whole_pop

    # Perform the evolution process for a given number of generations.
    def evolution(self, generations: int):
        best_individual = None
        best_fitness = np.inf

        for generation in range(generations):
            # Perform crossover in both populations
            self.partial_pop.crossover()
            self.whole_pop.crossover(self.partial_pop)

            # Reset fitness before evaluation
            self.partial_pop.reset_fitness()
            self.whole_pop.reset_fitness()

            # Evaluate fitness of the whole population
            avg_fitness, evaluated_whole_pop = self.eval(self.whole_pop, self.partial_pop)

            # Find the best individual
            for individual in evaluated_whole_pop.population:
                if individual.fitness < best_fitness:
                    best_fitness = individual.fitness
                    best_individual = individual

            print(f"Generation {generation}: Avg fitness: {avg_fitness}, Best fitness: {best_fitness}")

        return best_individual
