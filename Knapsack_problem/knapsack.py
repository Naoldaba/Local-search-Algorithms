import argparse
from collections import defaultdict
import time
from genetic_algorithm import knapsack_genetic_algorithm
from simulated_annealing import knapsack_simulated_annealing
from hill_climbing import knapsack_hill_climbing


def main(args):
    algorithm = args.algorithm
    file_name = args.file

    # Add your logic here based on the selected algorithm and file
    print(f"Algorithm: {algorithm}")
    print(f"File: {file_name}")

    def read_knapsack_file(file_path):
        items = []
        with open(file_path, 'r') as file:
            knapsackCapacity = int(file.readline().strip())

            # Skip the first line
            file.readline()
            # Read each item's details
            while True:
                line = file.readline().strip()
                if not line:
                    break  # Exit the loop if there are no more lines
                name, weight, value, n_items = line.split(',')
                items.append({'name': name, 'weight': float(
                    weight), 'value': int(value), 'n_items': int(n_items)})
        return items, knapsackCapacity

    def flatten_items(items):
        weights = []
        values = []
        index_to_name = {}
        for idx, item in enumerate(items):
            weight = item['weight']
            value = item['value']
            n_items = item['n_items']
            name = item['name']
            weights.extend([weight] * n_items)
            values.extend([value] * n_items)
            for i in range(n_items):
                index_to_name[len(weights) - n_items + i] = name
        return weights, values, index_to_name
    def benchmark_algorithm(algorithm, items, value,max_weight):
        start_time = time.time()
        solution,something = algorithm(items,value, max_weight)
        end_time = time.time()
        execution_time = end_time - start_time
        return execution_time


# ///////////////////////////////////////////////////////////////////////////

    items, capacity = read_knapsack_file(file_name)
    weights, values, index_to_name = flatten_items(items)
    excution_time= benchmark_algorithm(knapsack_genetic_algorithm, weights,values, capacity)
    solution, best_fitness = None, 0
    if algorithm == 'sa':
        solution, best_fitness = knapsack_simulated_annealing(
            weights, values, capacity)
    elif algorithm == "hc":
        solution, best_fitness = knapsack_hill_climbing(
            weights, values, capacity)
    elif algorithm == "ga":
        solution, best_fitness = knapsack_genetic_algorithm(
            weights, values, capacity)

    else:
        print("Invalid algorithm. Please choose 'sa' for simulated annealing.")

    if solution:
        print("Knapsack capacity: ", capacity)

        print("Selected items:")
        selectedItem = defaultdict(int)
        for i in range(len(solution)):
            if solution[i] == 1:
                selectedItem[index_to_name[i]] += 1
        for key in selectedItem:
            print(f"{key}: {selectedItem[key]}")
        print(f"Total value: {best_fitness}")
        print(f"Execution time: {excution_time}")

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Knapsack problem solver")
    parser.add_argument(
        "--algorithm", choices=["hc", "sa", "ga"], help="Algorithm to use (ga or hc or sa)", required=True)
    parser.add_argument("--file", help="Input file name", required=True)
    args = parser.parse_args()

    main(args)
