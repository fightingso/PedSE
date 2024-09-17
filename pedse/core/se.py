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

    def __init__(self, fitness_eval, chrom_len: int, partial_pop: PartialPopulation, whole_pop: WholePopulation):

        self.fitness_eval = fitness_eval
        self.chrom_len = chrom_len
        self.partial_pop = partial_pop
        self.whole_pop = whole_pop

    # Perform the evolution process for a given number of generations.
    def evolution(self, generations: int):
        best = []

        for generation in range(generations):
            best.append(self.partial_pop.population[0].fitness)
            # Perform crossover in both populations
            self.partial_pop.crossover()
            self.whole_pop.crossover(self.partial_pop)

            # Reset fitness before evaluation
            self.partial_pop.reset_fitness()
            self.whole_pop.reset_fitness()
            self.fitness_eval()
            print("Generation:" + str(generation) + "Fitness:" + str(best[generation]))
