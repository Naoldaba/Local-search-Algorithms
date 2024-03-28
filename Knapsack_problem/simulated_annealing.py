import random
import math


def knapsack_simulated_annealing(weights, values, capacity, max_iter=100, initial_temp=200, cooling_rate=0.99):
    n = len(weights)
    current_solution = [random.choice([0, 1]) for _ in range(n)]
    best_solution = current_solution.copy()
    best_fitness = get_fitness(current_solution, weights, values, capacity)

    current_temp = initial_temp

    for _ in range(max_iter):
        # Generate a new candidate solution
        candidate_solution = current_solution.copy()
        index = random.randint(0, n-1)
        candidate_solution[index] = 1 - candidate_solution[index]

        # Calculate the change in fitness
        candidate_fitness = get_fitness(
            candidate_solution, weights, values, capacity)
        delta_fitness = candidate_fitness - best_fitness

        # Accept or reject the candidate solution
        if delta_fitness > 0 or random.random() < math.exp(delta_fitness / current_temp):
            current_solution = candidate_solution
            best_fitness = candidate_fitness

        # Update the best solution
        if best_fitness > get_fitness(best_solution, weights, values, capacity):
            best_solution = current_solution.copy()

        # Update the temperature
        current_temp *= cooling_rate

    return best_solution, best_fitness


def get_fitness(solution, weights, values, capacity):
    total_weight = sum([weights[i]
                       for i in range(len(solution)) if solution[i] == 1])
    if total_weight > capacity:
        return -float('inf')
    total_value = sum([values[i]
                      for i in range(len(solution)) if solution[i] == 1])
    return total_value
