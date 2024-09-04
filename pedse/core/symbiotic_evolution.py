import numpy as np
from ppop import Population as PartialPopulation
from wpop import WholePopulation

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


# Example of fitness evaluation function to be used with SymbioticEvolution
def evaluate_fitness(whole_population: WholePopulation, partial_population: PartialPopulation):
    """
    Evaluates the fitness of the entire population by summing the fitness of the partial population in each whole individual.
    """
    total_fitness = 0
    for individual in whole_population.population:
        fitness = np.sum([ind.fitness for ind in individual.chrom])
        individual.fitness = fitness
        total_fitness += fitness
    avg_fitness = total_fitness / len(whole_population.population)
    return avg_fitness, whole_population


if __name__ == "__main__":
    # Initialize partial population
    partial_pop_size = 20
    partial_chrom_len = 10
    mutate_prob_partial = 0.1
    crossover_prob_partial = 0.8
    partial_population = PartialPopulation(partial_pop_size, partial_chrom_len, mutate_prob_partial, crossover_prob_partial)

    # Initialize whole population
    whole_pop_size = 10
    whole_chrom_len = 5
    mutate_prob_whole = 0.05
    crossover_prob_whole = 0.9
    whole_population = WholePopulation(whole_pop_size, whole_chrom_len, mutate_prob_whole, crossover_prob_whole, partial_population)

    # Initialize Symbiotic Evolution with fitness evaluation function
    se = SymbioticEvolution(eval=evaluate_fitness, chrom_len=whole_chrom_len, partial_pop=partial_population, whole_pop=whole_population)

    # Run the evolution for 100 generations
    
    best_individual = se.evolution(generations=100)

   