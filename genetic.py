import base64
from calendar import c
from lib2to3.pygram import Symbols
import re
import numpy as np
import random
from sympy import *

class Genetic:
    def __init__(self, population_size, chromosome_size, iterations, mutation_chance, crossing_over_chance, selection_factor, fitnes):
        self.population = []
        self.population_size = population_size
        self.chromosome_size = chromosome_size
        self.iterations = iterations
        self.mutation_chance = mutation_chance
        self.crossing_over_chance = crossing_over_chance
        self.selection_factor = selection_factor
        self.fitnes_f = simplify(fitnes, transformations='all')

    def generate_population(self):
        self.population = [[random.randint(0,1) for _ in range(self.chromosome_size)] for _ in range(self.population_size)]

    
    def decode(self, chromosome, num_of_variables) -> list:
        split_chromosome = np.array_split(np.array(chromosome), num_of_variables) 

        result = []
        for bin_variable in split_chromosome:
            bin_variable = bin_variable.tolist()
            val = 0
            for i in bin_variable:
                val += i*pow(2.0,-(i+1))
            result.append(val)
        return result

    def fitnes(self, chromosome):
        symbols = self.fitnes_f.free_symbols

        variables = list(zip(
            list(symbols),
            self.decode(chromosome, len(symbols))
            ))
        return self.fitnes_f.subs(variables)

    def mutation(self):
        for i in range(self.population_size):
            for j in range(self.chromosome_size):
                if random.random() < self.mutation_chance:
                   self.population[i][j] = 1 - self.population[i][j]

    def crossing_over(self):
        for i in range(0, self.population_size, 2):
            if random.random() < self.crossing_over_chance:
                delimiter = random.randint(1, self.chromosome_size - 1)
                self.population[i-1] = self.population[i-1][:delimiter] + self.population[i][delimiter:]
                self.population[i] = self.population[i][:delimiter] + self.population[i-1][delimiter:]
    
    def epoch(self):
        self.mutation()
        self.crossing_over()



        
                





