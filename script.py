import requests
import csv
import wget
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def get_1000_posts():
    token = os.environ['token']
    domain = ['domain']
    version = 5.101
    count = 100
    offset = 0
    all_posts = []

    while offset != 1000:
        response = requests.get('https://api.vk.com/method/wall.get', params={
            'access_token': token,
            'v': version,
            'domain': domain,
            'count': count,
            'offset': offset
        })
        data = response.json()['response']['items']
        offset += 100
        all_posts.extend(data)
    return all_posts


# all_posts = get_1000_posts()


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
    counter = 0
    with open('urls.csv', 'r') as file:
        reader = csv.reader(file)
        for photo in reader:
            try:
                url = photo[0]
                wget.download(url, os.path.join(BASE_DIR, f'img/pic{counter}.jpg'))
                counter += 1
            except:
                pass


# file_writer(all_posts)
# file_reader()
download_photos()

print(1)
