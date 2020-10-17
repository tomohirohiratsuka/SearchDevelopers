import pandas as pd
import os
from os import listdir
from os.path import isfile, join
import json


def format_csv():
    path = 'json'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for file in files:
        with open(path + '/' + file, mode='r') as f:
            file_name, ext = os.path.splitext(file)
            data = json.load(f)
            df = pd.DataFrame(data['items'])
            df.to_csv('csv/' + file_name + '.csv')

if __name__ == '__main__':
    format_csv()
