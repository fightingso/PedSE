import hydra
import numpy as np

from omegaconf import DictConfig


class Individual:
    def __init__(self, chrom_len, mutate_prob):
        self.chrom = np.random.randint(0, 2, chrom_len)
        self.fitness = 1e9
        self.chrom_len = chrom_len
        self.mutate_prob = mutate_prob

    def crossover(self, parent1, parent2, index1, index2):
        if index1 > index2:
            index1, index2 = index2, index1
        self.chrom[:index1] = parent1.chrom[:index1]
        self.chrom[index1:index2] = parent2.chrom[index1:index2]
        self.chrom[index2:] = parent1.chrom[index2:]
        self.mutate()

    def mutate(self):
        for i in range(self.chrom_len):
            if np.random.rand() < self.mutate_prob:
                self.chrom[i] = 1 - self.chrom[i]


class Population:
    def __init__(self, pop_size, chrom_len, mutate_prob, crossover_prob):
        self.population = [Individual(chrom_len, mutate_prob) for _ in range(pop_size)]
        self.crossover_prob = crossover_prob

    def crossover(self):
        for i in range(int(len(self.population) * (1 - self.crossover_prob)), len(self.population)):
            parent1, parent2 = np.random.choice(len(self.population) // 4, size=2)
            index1, index2 = np.random.randint(0, self.population[0].chrom_len, size=2)
            self.population[i].crossover(self.population[parent1], self.population[parent2], index1, index2)

    def reset_fitness(self):
        for individual in self.population:
            individual.fitness = 1e9


class WholeIndividual:
    def __init__(self, chrom_len, mutate_prob, ppop):
        self.chrom = [np.random.choice(ppop.population) for _ in range(chrom_len)]
        self.chrom_len = chrom_len
        self.mutate_prob = mutate_prob
        self.fitness = 1e9

    def crossover(self, parent1, parent2, index1, index2, ppop):
        if index1 > index2:
            index1, index2 = index2, index1
        self.chrom[:index1] = parent1.chrom[:index1]
        self.chrom[index1:index2] = parent2.chrom[index1:index2]
        self.chrom[index2:] = parent1.chrom[index2:]
        self.mutate(ppop)

    def mutate(self, ppop):
        for i in range(self.chrom_len):
            if np.random.rand() < self.mutate_prob:
                self.chrom[i] = np.random.choice(ppop.population)


class WholePopulation:
    def __init__(self, chrom_len, pop_size, crossover_prob, mutate_prob, ppop):
        self.population = [WholeIndividual(chrom_len, mutate_prob, ppop) for _ in range(pop_size)]
        self.chrom_len = chrom_len
        self.pop_size = pop_size
        self.crossover_prob = crossover_prob

    def crossover(self, ppop):
        for i in range(int(self.pop_size * (1 - self.crossover_prob)), self.pop_size):
            parent1, parent2 = np.random.choice(self.pop_size // 4, size=2)
            index1, index2 = np.random.randint(0, self.chrom_len, size=2)
            self.population[i].crossover(self.population[parent1], self.population[parent2], index1, index2, ppop)

    def reset_fitness(self):
        for individual in self.population:
            individual.fitness = 1e9


def evaluate_fitness(particle_chrom_len, whole_chrom_len, ppop, wpop):
    for w_ind in wpop.population:
        fitness = 0.0
        for j in range(whole_chrom_len):
            for k in range(particle_chrom_len):
                fitness += (w_ind.chrom[j].chrom[k] * 2 - 1) * np.sqrt(j * particle_chrom_len + k + 1)
        w_ind.fitness = np.abs(fitness)
        for j in range(whole_chrom_len):
            if w_ind.chrom[j].fitness > w_ind.fitness:
                w_ind.chrom[j].fitness = w_ind.fitness

    ppop.population.sort(key=lambda ind: ind.fitness)
    wpop.population.sort(key=lambda ind: ind.fitness)


@hydra.main(config_name="config", config_path="config", version_base=None)
def main(config: DictConfig):
    particle_hparams = config.particle_hparams
    whole_hparams = config.whole_hparams

    ppop = Population(
        particle_hparams.pop_size,
        particle_hparams.chrom_len,
        particle_hparams.mutate_prob,
        particle_hparams.crossover_prob
    )
    wpop = WholePopulation(
        whole_hparams.chrom_len,
        whole_hparams.pop_size,
        whole_hparams.crossover_prob,
        whole_hparams.mutate_prob,
        ppop
    )

    evaluate_fitness(
        particle_hparams.chrom_len,
        whole_hparams.chrom_len,
        ppop,
        wpop
    )

    best = []

    for generation in range(config.max_generation):
        print(f"{generation+1}: {wpop.population[0].fitness}")
        best.append(wpop.population[0].fitness)
        ppop.crossover()
        wpop.crossover(ppop)
        ppop.reset_fitness()
        wpop.reset_fitness()
        evaluate_fitness(
            particle_hparams.chrom_len,
            whole_hparams.chrom_len,
            ppop,
            wpop
        )


if __name__ == "__main__":
    main()

