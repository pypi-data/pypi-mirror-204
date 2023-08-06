import json
import pkg_resources
import pandas as pd
import matplotlib.pyplot as plt

def prints_something(message):
    print(message)


def list_available_cities():
    data_path = pkg_resources.resource_filename(
        'zicheng', "data/city_subzone_attr.json")
    with open(data_path, 'r') as f:
        data = json.load(f)
    print(f'Available cities: {list(data.keys())}')


def get_city_subzone_data(city):
    data_path = pkg_resources.resource_filename('zicheng', "data/city_subzone_attr.json")
    with open(data_path, 'r') as f:
        data = json.load(f)
    return pd.read_csv(data[city], index_col=0)

 
