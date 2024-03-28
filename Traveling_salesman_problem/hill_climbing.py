from collections import defaultdict
import math
import numpy as np, random, operator, pandas as pd
import matplotlib.pyplot as plt
from file_reader import read_cities


def hill_climbing(city_coordinates):

    city_distances = defaultdict(float)

    def calculate_distance(city1, city2):
        # Calculate the Euclidean distance between two cities
        lat1, lon1 = city_coordinates[city1]
        lat2, lon2 = city_coordinates[city2]
        return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)
    for city1 in city_coordinates:
        for city2 in city_coordinates:
            if city1 != city2:
                city_distances[(city1,city2)] = calculate_distance(city1, city2)
                city_distances[(city2,city1)] = calculate_distance(city1, city2)


    print(city_coordinates)

    import random
    def generate_initial_population(population_size):
        # Generate an initial population of random tours
        initial_population = []
        cities_list = list(city_coordinates.keys())  # Get the list of city names
        for _ in range(population_size):
            tour = random.sample(cities_list, len(cities_list))  # Create a random permutation of city names
            initial_population.append(tour)
        return initial_population
    CONSTANT = 1 # initialized with 1 for simplicity
    routes = generate_initial_population(CONSTANT)

    print(routes)

    def fitness_of_route(route):
        total = 0
        for i in range(1, len(route)):
            start = route[i-1]
            end = route[i]
            total += city_distances[start,end]
        return total

    import matplotlib.pyplot as plt

    def plot_tsp_path(cities, path, total_distance, start_color='green', end_color='red'):

        # Extract city coordinates
        x = [cities[city][1] for city in cities]  # longitude
        y = [cities[city][0] for city in cities]  # latitude
        
        # Plot cities
        plt.scatter(x, y, color='blue', label='Cities')
        
        # Plot path
        path_x = [cities[city][1] for city in path]
        path_y = [cities[city][0] for city in path]
        plt.plot(path_x, path_y, color='black', linewidth=1, linestyle='-', marker='o', label='Path')
        
        # Annotate cities
        for city, xi, yi in zip(cities.keys(), x, y):
            plt.annotate(city, (xi, yi), textcoords="offset points", xytext=(0,5), ha='center')
        
        # Annotate total distance at the bottom
        plt.text(0.5, -0.05, f'Total Distance: {total_distance:.2f}', horizontalalignment='center', verticalalignment='top', transform=plt.gca().transAxes)
        
        # Color the starting and ending cities
        start_city = path[0]
        end_city = path[-1]
        start_index = list(cities.keys()).index(start_city)
        end_index = list(cities.keys()).index(end_city)
        plt.scatter(x[start_index], y[start_index], color=start_color, label='Start City')
        plt.scatter(x[end_index], y[end_index], color=end_color, label='End City')
        
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Traveling Salesman Problem')
        plt.legend()
        plt.grid(True)
        plt.show()


    initial_route = routes[0]
    initial_route.append(initial_route[0])
    best_route = initial_route[:]
    best_distance = fitness_of_route(initial_route)
    max_iterations = 5  # Adjust as needed
    improved = False
    plot_tsp_path(city_coordinates,best_route, fitness_of_route(best_route))


    for _ in range(max_iterations):
        for i in range(len(best_route)):
            for j in range(i + 1, len(best_route)):
                new_route = best_route[:]
                new_route[i], new_route[j] = new_route[j], new_route[i]  # Swap cities
                new_distance = fitness_of_route(new_route)
                if new_distance < best_distance:
                    plot_tsp_path(city_coordinates,new_route, fitness_of_route(new_route))
                    best_route = new_route[:]
                    best_distance = new_distance
                    improved = True
        if not improved:
            break  

