import numpy as np
import pytest

from pedse import Individual, Population


# Test the initialization of the Individual class.
@pytest.mark.parametrize(
    "chrom_len, mutate_prob",
    [
        (10, 0.1),
        (20, 0.2),
        (30, 0.3),
    ],
)
def test_individual(chrom_len, mutate_prob):
    ind = Individual(chrom_len, mutate_prob)

    # Check if the chromosome is of the correct length and contains only 0s and 1s.
    assert len(ind.chrom) == chrom_len
    assert all(gene in [0, 1] for gene in ind.chrom)

    # Check if the fitness is set to 1e9.
    assert ind.mutate_prob == mutate_prob
    # Check if the mutation probability is set correctly.
    assert ind.fitness == 1e9


# Test the initialization of the Population class.
@pytest.mark.parametrize(
    "pop_size, chrom_len, mutate_prob, crossover_prob",
    [
        (10, 10, 0.1, 0.8),
        (20, 20, 0.2, 0.6),
        (30, 30, 0.3, 0.4),
    ],
)
def test_population(pop_size, chrom_len, mutate_prob, crossover_prob):
    pop = Population(pop_size, chrom_len, mutate_prob, crossover_prob)

    # Check if the population size is correct.
    assert len(pop.population) == pop_size

    # Check if the chromosome length is correct for each individual.
    assert all(ind.chrom_len == chrom_len for ind in pop.population)

    # Check if the mutation probability is correct for each individual.
    assert all(ind.mutate_prob == mutate_prob for ind in pop.population)

    # Check if the crossover probability is correct for the population.
    assert pop.crossover_prob == crossover_prob
