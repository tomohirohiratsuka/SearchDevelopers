import pandas as pd
import os
from os import listdir
from os.path import isfile, join
from main import check_limits
import requests
import math


def get_user_details():
    url = 'https://api.github.com/users/'
    headers = {'Accept': 'application/vnd.github.v3+json', 'content-type': 'application/json',
               'Authorization': 'token {}'.format(os.environ['ACCESS_TOKEN'])}
    path = 'csv'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    file_counter = 0
    for file in files:
        df = pd.read_csv(path + '/' + file)
        filtered = df[df['type'] != 'Organization']
        user_details = []
        for user_id in filtered['login']:
            check_limits()
            response = requests.get(url + user_id, headers=headers)
            if response.status_code == 200:
                user_details.append(response.json())
                ratio = math.ceil((len(user_details) / len(filtered['login'])) * 100)
                print('{}% done in {}'.format(ratio, file))
            elif response.status_code == 404:
                print('User id {} Not found'.format(user_id))
                break
            else:
                print(response.text)
                break

        file_counter += 1
        result_df = pd.DataFrame(user_details)
        file_name, ext = os.path.splitext(file)
        result_df.to_csv('users/' + file_name + '.csv')
        print('{}/{} file is done'.format(file_counter, len(files)))


if __name__ == '__main__':
    get_user_details()
