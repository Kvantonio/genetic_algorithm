# pylint: disable=W0614, C0116, C0114, C0115

import random
import numpy as np
import sympy

class Individ:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = 0

    def __str__(self):
        return f"chromosome: {self.chromosome} \nfitness: {self.fitness}"


class Genetic:
    def __init__(self, params):
        self.population = []
        self.population_size = params['population']
        self.chromosome_size = params['chromosome']
        self.iterations = params['iterations']
        self.mutation_chance = params['mutation']
        self.crossing_over_chance = params['crossing_over']
        self.selection_factor = params['selection']
        self.fitness_f = sympy.simplify(params['fitness'], transformations='all')
        self.max_fitness = []
        self.avg_fitness = []
        self.trend = params['trend']

    def generate_population(self):
        self.population = [
                        Individ([random.randint(0,1) for _ in range(self.chromosome_size)])
                        for _ in range(self.population_size)
                    ]

    def get_population(self):
        return self.population

    def decode(self, chromosome, num_of_variables) -> list:
        split_chromosome = np.array_split(np.array(chromosome), num_of_variables)

        result = []
        for position, bin_variable in enumerate(split_chromosome):
            bin_variable = bin_variable.tolist()
            val = 0
            for index, value in enumerate(bin_variable):
                val += value*pow(2.0,-(index-position+1))
            result.append(val*100-50)
        return result

    def fitness(self, chromosome):
        func_symbols = self.fitness_f.free_symbols

        variables = list(zip(
            list(func_symbols),
            self.decode(chromosome.chromosome, len(func_symbols))
            ))

        fitness = self.fitness_f.subs(variables)
        chromosome.fitness = fitness
        return fitness

    def mutation(self):
        for i in range(self.population_size):
            for j in range(self.chromosome_size):
                if random.random() < self.mutation_chance:
                    self.population[i].chromosome[j] = 1 - self.population[i].chromosome[j]

    def crossing_over(self):
        # if not working use randome choice
        for i in range(1, self.population_size, 2):
            if random.random() < self.crossing_over_chance:
                delimiter = random.randint(1, self.chromosome_size - 1)
                first = self.population[i-1].chromosome
                second = self.population[i].chromosome

                self.population[i-1].chromosome = first[:delimiter] + second[delimiter:]
                self.population[i].chromosome = second[:delimiter] + first[delimiter:]

    def selection(self):
        # self.population.sort(key=self.fitness, reverse=True)
        reversed = False
        if self.trend == "max":
            reversed = True
        sorted_p = sorted(self.population, key=self.fitness, reverse=reversed)

        min_fitnes = sorted_p[-1].fitness
        max_fitnes = sorted_p[0].fitness

        fitness_sum = sum(map(lambda x: x.fitness, self.population))

        self.avg_fitness.append(fitness_sum/self.population_size)
        self.max_fitness.append(max_fitnes)

        new_population = []
        while len(new_population) < self.population_size:
            num = random.randint(0, self.population_size-1)
            if self.selection_factor*random.random() < (self.population[num].fitness-min_fitnes)/(max_fitnes-min_fitnes):
                new_population.append(Individ(self.population[num].chromosome))

        self.population = new_population


    def epoch(self):
        self.mutation()
        self.crossing_over()
        self.selection()
