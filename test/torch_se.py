import hydra
import torch
import random

from omegaconf import DictConfig


class Individual:
    def __init__(self, chrom_len, mutate_prob, device):
        self.chrom = torch.randint(0, 2, (chrom_len,), device=device)
        self.fitness = torch.tensor(1e9, device=device)
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
            if torch.rand(1).item() < self.mutate_prob:
                self.chrom[i] = 1 - self.chrom[i]


class Population:
    def __init__(self, pop_size, chrom_len, mutate_prob, crossover_prob, device):
        self.population = [Individual(chrom_len, mutate_prob, device) for _ in range(pop_size)]
        self.crossover_prob = crossover_prob

    def crossover(self):
        for i in range(int(len(self.population) * (1 - self.crossover_prob)), len(self.population)):
            parent1, parent2 = torch.randint(0, len(self.population) // 4, (2,))
            index1, index2 = torch.randint(0, self.population[0].chrom_len, (2,))
            self.population[i].crossover(self.population[parent1], self.population[parent2], index1, index2)

    def reset_fitness(self):
        for individual in self.population:
            individual.fitness = torch.tensor(1e9, device=individual.fitness.device)


class WholeIndividual:
    def __init__(self, chrom_len, mutate_prob, ppop, device):
        self.chrom = [random.choice(ppop.population) for _ in range(chrom_len)]
        self.chrom_len = chrom_len
        self.mutate_prob = mutate_prob
        self.fitness = torch.tensor(1e9, device=device)

    def crossover(self, parent1, parent2, index1, index2, ppop):
        if index1 > index2:
            index1, index2 = index2, index1
        self.chrom[:index1] = parent1.chrom[:index1]
        self.chrom[index1:index2] = parent2.chrom[index1:index2]
        self.chrom[index2:] = parent1.chrom[index2:]
        self.mutate(ppop)

    def mutate(self, ppop):
        for i in range(self.chrom_len):
            if torch.rand(1).item() < self.mutate_prob:
                self.chrom[i] = random.choice(ppop.population)


class WholePopulation:
    def __init__(self, chrom_len, pop_size, crossover_prob, mutate_prob, ppop, device):
        self.population = [WholeIndividual(chrom_len, mutate_prob, ppop, device) for _ in range(pop_size)]
        self.chrom_len = chrom_len
        self.pop_size = pop_size
        self.crossover_prob = crossover_prob

    def crossover(self, ppop):
        for i in range(int(self.pop_size * (1 - self.crossover_prob)), self.pop_size):
            parent1, parent2 = torch.randint(0, self.pop_size // 4, (2,))
            index1, index2 = torch.randint(0, self.chrom_len, (2,))
            self.population[i].crossover(self.population[parent1], self.population[parent2], index1, index2, ppop)

    def reset_fitness(self):
        for individual in self.population:
            individual.fitness = torch.tensor(1e9, device=individual.fitness.device)


def evaluate_fitness(particle_chrom_len, whole_chrom_len, ppop, wpop, device):
    for w_ind in wpop.population:
        fitness = 0.0
        for j in range(whole_chrom_len):
            for k in range(particle_chrom_len):
                fitness += (w_ind.chrom[j].chrom[k].item() * 2 - 1) * torch.sqrt(torch.tensor(j * particle_chrom_len + k + 1, dtype=torch.float, device=device))
        w_ind.fitness = torch.abs(torch.tensor(fitness, device=device))
        for j in range(whole_chrom_len):
            if w_ind.chrom[j].fitness > w_ind.fitness:
                w_ind.chrom[j].fitness = w_ind.fitness

    ppop.population.sort(key=lambda ind: ind.fitness)
    wpop.population.sort(key=lambda ind: ind.fitness)


@hydra.main(config_name="config", config_path="config", version_base=None)
def main(config: DictConfig):
    device = torch.device(config.device)

    particle_hparams = config.particle_hparams
    whole_hparams = config.whole_hparams

    ppop = Population(
        particle_hparams.pop_size,
        particle_hparams.chrom_len,
        particle_hparams.mutate_prob,
        particle_hparams.crossover_prob,
        device
    )
    wpop = WholePopulation(
        whole_hparams.chrom_len,
        whole_hparams.pop_size,
        whole_hparams.crossover_prob,
        whole_hparams.mutate_prob,
        ppop,
        device
    )

    evaluate_fitness(
        particle_hparams.chrom_len,
        whole_hparams.chrom_len,
        ppop,
        wpop,
        device
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
            wpop,
            device
        )


if __name__ == "__main__":
    main()

