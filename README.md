# PedSE : Parallelized Symbiotic Evolution
PedSE is the package for implementing a parallelized symbiotic evolution with Python.

## Synbiotic Evolution
Symbiotic evolution, introduced by Moriarty et al. [[Moriarty 96](https://link.springer.com/article/10.1007/BF00114722)], is a co-evolutionary approach for optimizing solutions, such as neural networks. In this method, a solution is built from smaller components, each represented by a similar genetic sequence. These components evolve together in a single population, where each one is a potential part of the final solution.

For example, in a neural network, individual neurons in hidden layers are treated as components, and their combination forms the entire network. Symbiotic evolution allows these components to evolve simultaneously, creating a more effective overall solution by focusing on optimizing each part.
