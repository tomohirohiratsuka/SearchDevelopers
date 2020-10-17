import json
import requests
from datetime import datetime
import math
import time
import os
from dotenv import load_dotenv
load_dotenv()


def check_limits():
    rate = requests.get('https://api.github.com/rate_limit',
                        headers={'Accept': 'application/vnd.github.v3+json',
                                 'Authorization': 'token {}'.format(os.environ['ACCESS_TOKEN'])}).json()

    for key in rate['resources'].keys():
        if rate['resources'][key]['remaining'] == 0:
            print('{} API call reached limitation, Waiting for {}sec ...'.format(key, 60))
            time.sleep(60)
        else:
            continue


def search_developers():
    json_path = 'json/'
    url = 'https://api.github.com/search/users'
    headers = {'Accept': 'application/vnd.github.v3+json', 'content-type': 'application/json',
               'Authorization': 'token {}'.format(os.environ['ACCESS_TOKEN'])}
    queries = ['vue', 'laravel', 'php', 'javascript', 'serviceworker']
    for query in queries:
        check_limits()
        output_file_name = '{}_{}.json'.format(datetime.now().strftime('%Y%m%d'), query)
        params = {'q': query, 'sort': 'followers', 'order': 'desc'}
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            total_count = response.json()['total_count']
            total_pages = math.ceil(total_count / 100)
            target_query_users = []
            # only first 1000 rows with github api limitation
            for index in range(1, 10):
                check_limits()
                specified_params = {'q': query, 'per_page': 100, 'page': index}
                print('Request on page {} params: {}'.format(index, specified_params))
                target_page_response = requests.get(url, params=specified_params, headers=headers)
                if target_page_response.status_code == 200:
                    users = target_page_response.json()['items']
                    print('{} Users Get this request'.format(len(users)))
                    target_query_users.extend(users)
                    print('Request Succeeded on page {} params: {}'.format(index, specified_params))
                elif target_page_response.status_code == 304:
                    print('Already Cached')
                    print('Current index: {}, Total pages: {}'.format(index, total_pages))
                    print(target_page_response.text)
                    break
                elif target_page_response.status_code == 422:
                    print('Unprocessable Entity')
                    print('Current index: {}, Total pages: {}'.format(index, total_pages))
                    print(target_page_response.text)
                    break
                elif target_page_response.status_code == 503:
                    print('Service Unavailable')
                    print('Current index: {}, Total pages: {}'.format(index, total_pages))
                    print(target_page_response.text)
                    break
                else:
                    print('Something Went Wrong')
                    print('Current index: {}, Total pages: {}'.format(index, total_pages))
                    print(target_page_response.text)
                    break
            if os.path.isfile(json_path + output_file_name):
                with open(output_file_name, mode='w') as f:
                    data = json.load(f)
                    data['items'].extend(target_query_users)
                    data['total_pages'] = total_pages
                    data['current_index'] = index
                    json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True, separators=(',', ': '))
            else:
                with open(json_path + output_file_name, mode='w') as f:
                    json.dump({'items': target_query_users, 'total_pages': total_pages, 'current_index': index}, f,
                              indent=4, ensure_ascii=False, sort_keys=True, separators=(',', ': '))
        else:
            print(response.text)


if __name__ == '__main__':
    search_developers()
