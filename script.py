import requests
import csv
import wget
import os
from config import config
import logging
import json
import sys
import pprint
import click

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def get_1000_posts():
    """
    The function scrape urls of imgs from group Ubezhise and return list of json.
    In core of function is method wall.get from standard vk api. It take next arguments:
    owner_id - id of group (must be -xxxxxxx) or page where we will scrape images
    v - version of api
    domain - short name of group
    The method can scrape only 100 post by one step, so it include argument offset - it means steps 0 - 100 - 200 - ...
    The function
    :return:
    """
    token = config['user_token'] or os.environ['token']
    domain = config['domain']
    version = 5.103
    count = 100
    offset = 0
    all_posts = []

    while offset <= 10000:
        try:
            response = requests.get('https://api.vk.com/method/wall.get', params={
                'owner_id': '-126048595',
                'access_token': token,
                'v': version,
                'domain': 'ubezhise',
                'count': count,
                'offset': offset
            })
            try:
                data = response.json()['response']['items']
                all_posts.extend(data)
            except:
                pass
            offset += 100
        except Exception as e:
            print('Error ', e.__class__.__name__, e)
            logging.error(e)
            sys.exit(-1)
    return all_posts


def file_writer(data):
    with open('urls.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow({'url'})
        for post in data:
            try:
                if post['attachments'][0]['type'] == 'photo':
                    img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
                else:
                    img_url = 'pass'
            except:
                pass
            a_pen.writerow([img_url])


def file_reader():
    with open('urls.csv', 'r') as file:
        reader = csv.reader(file)
        return reader


def download_photos():
    if not os.path.exists('img'):
        os.mkdir('img')
    counter = 0
    with open('urls.csv', 'r') as file:
        reader = csv.reader(file)
        for photo in reader:
            try:
                url = photo[0]
                wget.download(url, os.path.join(BASE_DIR, 'img/pic{}.jpg'.format(counter)))
                print('File pic{}.jpg successful downloaded!'.format(counter))
                logging.info('File pic{}.jpg successful downloaded!'.format(counter))
                counter += 1
            except Exception as e:
                print('File pic{}.jpg had problem with download!'.format(counter))
                logging.error('File pic{}.jpg had problem with download!'.format(counter))
                print(e.__class__.__name__, e)
                logging.error(e)
                pass


def main():

    logging.basicConfig(filename='log.txt', level=logging.ERROR)

    # all_posts = get_1000_posts()
    # file_writer(all_posts)
    # file_reader()
    download_photos()

    # print('Check your folder. There is must be .cvs file')


if __name__ == '__main__':
    main()
