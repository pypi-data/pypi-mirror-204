import json
import pkg_resources
import pandas as pd
import matplotlib.pyplot as plt
import ssl

# SSL bypass url verification
ssl._create_default_https_context = ssl._create_unverified_context

def prints_something(message):
    print(message)

def list_available_cities():
    data_path = pkg_resources.resource_filename('testapp_winstonyym', "data/city_subzone_attr.json")
    with open(data_path, 'r') as f:
        data = json.load(f)
    print(f'Available cities: {list(data.keys())}')

def get_city_subzone_data(city):
    data_path = pkg_resources.resource_filename('testapp_winstonyym', "data/city_subzone_attr.json")
    with open(data_path, 'r') as f:
        data = json.load(f)
    print(data[city])
    return pd.read_csv(data[city], index_col=0)

def plot_scatter(data, xaxis, yaxis):
    fig, ax = plt.subplots()
    ax.scatter(x=data[xaxis], y = data[yaxis])
    ax.set_xlabel(xaxis)
    ax.set_ylabel(yaxis)
    for i, label in enumerate(data.index):
        ax.annotate(label, (data[xaxis][i], data[yaxis][i]), size=8)
    plt.show()
