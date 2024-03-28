
import random


def knapsack_hill_climbing(weights, values, capacity, max_restarts=100):
    n = len(weights)
    best_solution = None
    best_fitness = float('-inf')
    restarts = 0

    while restarts < max_restarts:
        current_solution = [random.choice([0, 1]) for _ in range(n)]
        current_fitness = get_fitness(
            current_solution, weights, values, capacity)

        while True:
            # Generate a new candidate solution
            candidate_solution = current_solution.copy()
            index = random.randint(0, n-1)
            candidate_solution[index] = 1 - candidate_solution[index]

            # Calculate the change in fitness
            candidate_fitness = get_fitness(
                candidate_solution, weights, values, capacity)

            # Accept or reject the candidate solution
            if candidate_fitness > current_fitness:
                current_solution = candidate_solution
                current_fitness = candidate_fitness
            else:
                break  # Stop if no improvement

        if current_fitness > best_fitness:
            best_solution = current_solution
            best_fitness = current_fitness

        restarts += 1

    return best_solution, best_fitness


def get_fitness(solution, weights, values, capacity):
    total_weight = sum([weights[i]
                       for i in range(len(solution)) if solution[i] == 1])
    if total_weight > capacity:
        return -float('inf')
    total_value = sum([values[i]
                      for i in range(len(solution)) if solution[i] == 1])
    return total_value
