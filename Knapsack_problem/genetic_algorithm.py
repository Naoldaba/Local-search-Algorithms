import random


def knapsack_genetic_algorithm(weights, values, capacity, population_size=100, generations=100, crossover_rate=0.8, mutation_rate=0.2):
    n = len(weights)
    population = [[random.choice([0, 1]) for _ in range(n)]
                  for _ in range(population_size)]

    for _ in range(generations):
        # Evaluate fitness
        fitness_values = [get_fitness(
            chromosome, weights, values, capacity) for chromosome in population]
        max_fitness = max(fitness_values)
        max_index = fitness_values.index(max_fitness)
        best_solution = population[max_index]

        # Selection
        sorted_population = [chromosome for _, chromosome in sorted(
            zip(fitness_values, population), reverse=True)]
        # Keep the two fittest chromosomes
        selected_parents = sorted_population[:2]
        for _ in range(population_size - 2):
            parent1 = population[random.randint(0, population_size - 1)]
            parent2 = population[random.randint(0, population_size - 1)]
            selected_parents.append(parent1 if get_fitness(parent1, weights, values, capacity) > get_fitness(
                parent2, weights, values, capacity) else parent2)

        # Crossover
        new_population = []
        for i in range(0, population_size, 2):
            parent1, parent2 = selected_parents[i], selected_parents[i + 1]
            if random.random() < crossover_rate:
                crossover_point = random.randint(1, n - 1)
                child1 = parent1[:crossover_point] + parent2[crossover_point:]
                child2 = parent2[:crossover_point] + parent1[crossover_point:]
            else:
                child1, child2 = parent1, parent2
            new_population.extend([child1, child2])

        # Mutation
        for i in range(population_size):
            if random.random() < mutation_rate:
                mutation_point = random.randint(0, n - 1)
                new_population[i][mutation_point] = 1 - \
                    new_population[i][mutation_point]

        population = new_population

    return best_solution, max_fitness


def get_fitness(solution, weights, values, capacity):
    total_weight = sum([weights[i]
                       for i in range(len(solution)) if solution[i] == 1])
    if total_weight > capacity:
        return -float('inf')
    total_value = sum([values[i]
                      for i in range(len(solution)) if solution[i] == 1])
    return total_value
