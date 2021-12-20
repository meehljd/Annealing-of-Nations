import recheck_flights
import math
import json
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd

get_flight_updates = False
do_run_annealing = False

flight_file = r'.\data\flights.json'
geo_file = r'.\data\airport_geo.json'
path_file = r'.\data\best_path.json'

if get_flight_updates:
    flights = recheck_flights.recheck_flights(flight_file, geo_file)
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

def run_annealing(path):
    path = get_valid_path(path)
    cost = calculate_path_cost(path)
    best_cost = cost
    len_temp_sch = 1e6

    temperature_schedule = np.logspace(0.5, 3.5, num=len_temp_sch)[::-1]
    costs = []
    for i, k in enumerate(temperature_schedule):
        new_path = get_valid_path(path)
        cost = calculate_path_cost(path)
        new_cost = calculate_path_cost(new_path)
        p = acceptance_probability(cost, new_cost, k)
        if random.random() < p:
            path = new_path
        if new_cost < best_cost:
            best_path = path
            best_cost = new_cost
        costs.append(cost)
        if i % 1000 == 0:
            print(i/len_temp_sch, cost, new_cost, k, p, path == new_path, best_cost)

    visualize_cost(costs, temperature_schedule)

    return best_path, best_cost

def visualize_cost(costs, temperature_schedule):
    #TODO: update to include plt.animation() of path
    plt.plot(costs)
    plt.xlabel('iterations')
    plt.ylabel('cost (USD)')
    plt.title('Cost of Trip')
    plt.savefig(r'.\images\costs.png')
    plt.show()

    plt.plot(temperature_schedule)
    plt.xlabel('iterations')
    plt.ylabel('temperature')
    plt.title('Annealing Schedule')
    plt.savefig(r'.\images\schedule.png')
    plt.show()

if do_run_annealing:
    best_path, best_cost = run_annealing(path)
    with open(path_file, 'w') as outfile:
        json.dump(best_path, outfile, indent=2)
else:
    with open(path_file) as json_file:
        best_path = json.load(json_file)
    best_cost = calculate_path_cost(best_path)

print(f'For ${best_cost}, use {best_path}')

with open(geo_file) as json_file:
    airport_data = json.load(json_file)
airport_data = pd.DataFrame(airport_data)
gdf = gpd.GeoDataFrame(
    airport_data, geometry=gpd.points_from_xy(airport_data['longitude'], airport_data['latitude']))
print(gdf)
print(airport_data)

world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
world.head()

path_df = pd.DataFrame()
path_df['orig_ap'] = best_path
path_df['dest_ap'] = best_path[1:] + [best_path[-1]]
path_df = pd.merge(path_df, airport_data, left_on='orig_ap', right_on='airport', suffixes=('', '_orig'))
path_df = pd.merge(path_df, airport_data, left_on='dest_ap', right_on='airport', suffixes=('', '_dest'))
print(path_df)

#TODO merge origin_ap; dest_ap to airport_data

#TODO: Make df of path orig and dest lat & long.
# https://coderzcolumn.com/tutorials/data-science/how-to-create-connection-map-chart-in-python-jupyter-notebook-plotly-and-geopandas
with plt.style.context(("seaborn", "ggplot")):
    ## Plot world
    world.plot(figsize=(18,10), edgecolor="grey", color="white");

    for lat_o, long_o, lat_d, long_d in zip(path_df["latitude_orig"], path_df["longitude_orig"],
                                            path_df["latitude_dest"], path_df["longitude_dest"]):
        plt.plot([long_o , long_d], [lat_o, lat_d], color="red", alpha=0.5)
        plt.scatter(long_o, lat_o, color="blue", alpha=0.5)
plt.show()