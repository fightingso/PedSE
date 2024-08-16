import numpy as np
import torch 
WPOP_SIZE = 200
PPOP_SIZE = 400
MAX_GENERATION = 1000
WCROSSOVER_PROB = 0.5
PCROSSOVER_PROB = 0.9
WMUTATE_PROB = 0.01
PMUTATE_PROB = 0.04
WCHROM_LEN = 10
PCHROM_LEN = 10
class PartialIndividual:
    def __init__(self):
        
       
        
        self.chrom=torch.randint(low=0, high=2, size=(PCHROM_LEN,),device='cuda') 

        self.fitness = 1e9

    def crossover(self, parent1, parent2, index1, index2):
        if index1 > index2:
            index1, index2 = index2, index1
        for i in range(0, index1):
            self.chrom[i] = parent1.chrom[i]
        for i in range(index1, index2):
            self.chrom[i] = parent2.chrom[i]
        for i in range(index2, PCHROM_LEN):
            self.chrom[i] = parent1.chrom[i]
        self.mutate()

    def mutate(self):
        for i in range(PCHROM_LEN):
           

            if torch.rand(1,device='cuda').item() < PMUTATE_PROB: 
                self.chrom[i] = 1 - self.chrom[i]
                

class PartialPopulation:
    def __init__(self):
        self.population = []
        for _ in range(PPOP_SIZE):
            individual = PartialIndividual()
            self.population.append(individual)

    def crossover(self):
        for i in range(int(PPOP_SIZE * (1 - PCROSSOVER_PROB)), PPOP_SIZE):
           
            parent1=torch.randint(low=0, high=int(PPOP_SIZE/4), size=(1,),device='cuda').item() 
            
            parent2 = torch.randint(low=0, high=int(PPOP_SIZE/4), size=(1,),device='cuda').item() 
            
            index1 = torch.randint(low=0, high=int(PCHROM_LEN), size=(1,),device='cuda').item()  
            index2 = torch.randint(low=0, high=int(PCHROM_LEN), size=(1,),device='cuda').item()  
            
            self.population[i].crossover(self.population[parent1], self.population[parent2], index1, index2)

    def evainit(self):
        for i in range(PPOP_SIZE):
            self.population[i].fitness = 1e9


class WholeIndividual:
    def __init__(self):
        self.chrom = []
        for _ in range(WCHROM_LEN):
            index = torch.randint(low=0, high=int(PPOP_SIZE), size=(1,),device='cuda').item()  
            ppop = PartialPopulation()
            ppop.evainit()
            ppop.crossover()
            self.chrom.append(ppop.population[index])
        self.fitness = 1e9

    def crossover(self, parent1, parent2, index1, index2):
        if index1 > index2:
            index1, index2 = index2, index1
        for i in range(0, index1):
            self.chrom[i] = parent1.chrom[i]
        for i in range(index1, index2):
            self.chrom[i] = parent2.chrom[i]
        for i in range(index2, WCHROM_LEN):
            self.chrom[i] = parent1.chrom[i]
        self.mutate()

    def mutate(self):
        for i in range(WCHROM_LEN):
           
            if torch.rand(1,device='cuda')< WMUTATE_PROB:
                
                index = torch.randint(low=0, high=int(PPOP_SIZE), size=(1,),device='cuda').item() 
                self.chrom[i] = ppop.population[index]


class WholePopulation:
    def __init__(self):
        self.population = []
        for _ in range(WPOP_SIZE):
            individual = WholeIndividual()
            self.population.append(individual)

    def crossover(self):
        for i in range(int(PPOP_SIZE * (1 - PCROSSOVER_PROB)), PPOP_SIZE):
            
            parent1 = torch.randint(low=0, high=int(PPOP_SIZE/4), size=(1,),device='cuda').item()   
            parent2 = torch.randint(low=0, high=int(PPOP_SIZE/4), size=(1,),device='cuda').item()   
            index1 = torch.randint(low=0, high=int(PCHROM_LEN), size=(1,),device='cuda').item()              
            index2 = torch.randint(low=0, high=int(PCHROM_LEN), size=(1,),device='cuda').item()   
            self.population[i].crossover(self.population[parent1], self.population[parent2], index1, index2)

    def evainit(self):
        for i in range(WPOP_SIZE):
            self.population[i].fitness = 1e9


def evaluate_fitness():
    for i in range(WPOP_SIZE):
        fitness = 0.0
        for j in range(WCHROM_LEN):
            for k in range(PCHROM_LEN):
                
                fitness += (wpop.population[i].chrom[j].chrom[k] * 2 - 1) * torch.sqrt(torch.tensor(j*PCHROM_LEN+k+1,device='cuda')).item() 
                
        
        wpop.population[i].fitness = torch.abs(torch.tensor(fitness,device='cuda')).item() 
        for j in range(WCHROM_LEN):
            if wpop.population[i].chrom[j].fitness > wpop.population[i].fitness:
                wpop.population[i].chrom[j].fitness = wpop.population[i].fitness
    ppop.population.sort(key=lambda individual: individual.fitness)
    wpop.population.sort(key=lambda individual: individual.fitness)


ppop = PartialPopulation()
wpop = WholePopulation()
evaluate_fitness()


def main():
    best = []

    for i in range(MAX_GENERATION):
        print(f"{i+1}: {wpop.population[0].fitness}")
        best.append(wpop.population[0].fitness)
        ppop.crossover()
        wpop.crossover()
        ppop.evainit()
        wpop.evainit()
        evaluate_fitness()
    #print(torch.randint(low=0, high=2, size=(PCHROM_LEN,)),device='cuda')
    #print(torch.rand(1),device='cuda')
    #print(np.random.randint(0, int(PPOP_SIZE/4)),device='cuda')
    #print(torch.randint(low=0, high=int(PPOP_SIZE/4), size=(1,)),device='cuda')
   
if __name__=="__main__":
    main()

