import glob
import random
import requests
import os


# Клас для автоматического постинга
class PublicParserClass:
    user_token = os.environ['user_token']
    version = 5.101
    group_id = os.environ['group_id']
    url = 'https://api.vk.com/method/'
    user_id = os.environ['user_id']

    def post_my_photo(self):

        # Случайный выбор фотографии из директивы img
        all_photos = glob.glob('img/*.jpg')
        if all_photos != 0:
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

            # Удаление фотографии
            os.remove(photo_url)

            return post.json()
        else:
            return 'No more files...'


a = PublicParserClass().post_my_photo()
