import numpy as np
import pytest

from pedse.core import Individual


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
