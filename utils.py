import csv
import wget
import os
import glob
import random
import requests


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class PublicParser:
    service_token = os.environ['service_token']
    user_token = os.environ['user_token']
    id = os.environ['id']
    secure_key = os.environ['secure_key']
    url = 'https://api.vk.com/method/'
    version = 5.101
    group_id = os.environ['group_id']
    user_id = os.environ['user_id']


class PublicParserClass:
    user_token = os.environ['user_token']
    version = 5.101
    group_id = os.environ['group_id']
    url = 'https://api.vk.com/method/'
    user_id = os.environ['user_id']

    def post_my_photo(self):

        all_photos = glob.glob('img/*.jpg')
        photo_url = random.choice(all_photos)

        server_upload_server_url = requests.get(self.url + 'photos.getWallUploadServer', params={
            'group_id': self.group_id,
            'access_token': self.user_token,
            'v': self.version
        }).json()['response']['upload_url']

        photo_response = requests.post(server_upload_server_url, files={'photo': open(photo_url, 'rb')}).json()
        params = {
            'server': photo_response['server'],
            'photo': photo_response['photo'],
            'hash': photo_response['hash']
        }

        photo_id = requests.get(self.url + 'photos.saveWallPhoto', params={
            'access_token': self.user_token,
            'group_id': self.group_id,
            'photo': params['photo'],
            'server': params['server'],
            'hash': params['hash'],
            'v': self.version
        }).json()['response'][0]['id']

        post = requests.get(self.url + 'wall.post', params={
            'access_token': self.user_token,
            'v': self.version,
            'owner_id': -self.group_id,
            'from_group': 1,
            'attachments': 'photo' + str(self.user_id) + '_' + str(photo_id),
            'signed': 0
        })

        # print('photo' + str(self.group_id) + '_' + str(photo_id))

        return post.json()


def file_writer(data):
    with open('urls.csv', 'w', newline='') as file:
        a_pen = csv.writer(file)
        a_pen.writerow({'url'})
        for post in data:
            a_pen.writerow([post])


def parse():
    url = 'https://api.vk.com/method/'
    token = os.environ['token']
    v = 5.101
    offset = 0
    data1 = []
    data2 = []
    urls = []

    while offset != 2000:
        response = requests.get(url + 'wall.get', params={
            'access_token': token,
            'v': v,
            'domain': os.environ['domain'],
            'offset': offset,
            'count': 100
        })
        data1.extend(response.json()['response']['items'])
        offset += 100


    for d in data1:
        try:
            data2.extend(d['attachments'])
        except:
            pass


    for photo in data2:
        try:
            urls.append(photo['photo']['sizes'][-1]['url'])
        except:
            pass

    file_writer(urls)


def file_reader():
    with open('urls.csv', 'r') as file:
        reader = csv.reader(file)
        return reader


def download_photos():
    counter = 0
    try:
        os.system('mkdir img')
    except:
        pass
    with open('urls.csv', 'r') as file:
        reader = csv.reader(file)
        for photo in reader:
            try:
                url = photo[0]
                wget.download(url, os.path.join(BASE_DIR, f'img/pic{counter}.jpg'))
                counter += 1
            except:
                pass


def auth_vk_key():
    request = 'https://oauth.vk.com/authorize?...'
    data = {
        'client_id': 7141469,
        'redirect_uri': 'https://oauth.vk.com/blank.html',
        'v': 5.101,
        'response_type': 'token',
        'scope': 'wall,offline,manage'
    }


def wall_post():
    token = PublicParser.user_token
    owner_id = -os.environ['owner_id']
    message = 'Test message'
    url = 'https://api.vk.com/method/'

    try:
        response = requests.get(url + 'wall.post', params={
            'owner_id': owner_id,
            'access_token': token,
            'message': message,
            'v': 5.101,
            'from_group': 1,
            'signed': 0
        }).json()
    except:
        print('Error')

    print(response)


def post_photo():

    server_upload_server_url = requests.get(PublicParser.url + 'photos.getWallUploadServer', params={
        'group_id': PublicParser.group_id,
        'access_token': PublicParser.user_token,
        'v': PublicParser.version
    }).json()['response']['upload_url']

    photo_response = requests.post(server_upload_server_url, files={'photo': open(PublicParser.filename[0], 'rb')}).json()
    params = {
        'server': photo_response['server'],
        'photo': photo_response['photo'],
        'hash': photo_response['hash']
    }

    photo_id = requests.get(PublicParser.url + 'photos.saveWallPhoto', params={
        'access_token': PublicParser.user_token,
        'group_id': PublicParser.group_id,
        'photo': params['photo'],
        'server': params['server'],
        'hash': params['hash'],
        'v': PublicParser.version
    }).json()['response'][0]['id']

    post = requests.get(PublicParser.url + 'wall.post', params={
        'access_token': PublicParser.user_token,
        'v': PublicParser.version,
        'owner_id': -PublicParser.group_id,
        'from_group': 1,
        'attachments': 'photo' + str(PublicParser.user_id) + '_' + str(photo_id),
        'signed': 0
    })

    print('photo' + str(PublicParser.group_id) + '_' + str(photo_id))

    return post



# wall_post()
# data = post_photo().json()

a = PublicParserClass().post_my_photo()


print(1)
