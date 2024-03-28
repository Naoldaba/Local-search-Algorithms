def read_cities(filename):
    cities_data = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            city_name = parts[0]
            coordinates = tuple(map(float, parts[1:]))
            cities_data[city_name] = coordinates
    return cities_data