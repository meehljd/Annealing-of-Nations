import recheck_flights
import math
import json
import random
import numpy as np

get_flight_updates = False

flight_file = 'flights.json'

if get_flight_updates:
    flights = recheck_flights.recheck_flights(flight_file)
else:
    with open(flight_file) as json_file:
        flights = json.load(json_file)

path = [key for key in flights]

def calculate_path_cost(path):
    cost = 0
    for orig, dest in zip(path, path[1:]+[path[0]]):
        if dest in flights[orig]:
            cost += flights[orig][dest]
        else:
            return 9999
    return cost

def check_for_valid_path(path):
    for orig, dest in zip(path, path[1:]+[path[0]]):
        if dest not in flights[orig]:
            return False
    return True

def get_valid_path(path):
    is_path_valid = False
    invalid_count = 0
    while not is_path_valid:
        [i, j] = random.sample(range(len(path)), 2)
        path = swap_cities(path, i, j)
        is_path_valid = check_for_valid_path(path)
        invalid_count += 1
    return path

def swap_cities(path, i, j):
    assert isinstance(path, list)
    assert isinstance(i, int)
    assert isinstance(j, int)
    assert i >= 0 and j >= 0 and len(path) > 0
    assert i < len(path) and j < len(path) and i != j

    a, b = path[i], path[j]
    path2 = path.copy()
    path2[j] = a
    path2[i] = b

    return path2

def acceptance_probability(old_cost, new_cost, k):
    assert isinstance(old_cost, (int, float))
    assert isinstance(new_cost, (int, float))
    assert isinstance(k, (int, float))
    assert old_cost > 0 and new_cost > 0 and k > 0

    change = old_cost - new_cost
    if change < 0:
        p = math.exp(change / k)
    else:
        p = 1.0
    return p


path = get_valid_path(path)
cost = calculate_path_cost(path)

temperature_schedule = np.logspace(0, 4, num=100000)[::-1]
costs = []
for i, k in enumerate(temperature_schedule):
    new_path = get_valid_path(path)
    cost = calculate_path_cost(path)
    new_cost = calculate_path_cost(new_path)
    p = acceptance_probability(cost, new_cost, k)
    if random.random() < p:
        path = new_path
    costs.append(cost)
    if i % 100 == 0:
        print(i/len(temperature_schedule), cost, new_cost, p, path == new_path)

import matplotlib.pyplot as plt

plt.plot(costs)
plt.savefig('costs.png')
plt.show()

print(path)