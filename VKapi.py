import urllib.request
import os
import json
import requests


class VK:

    def __init__(self, access_token, version='5.131'):
        self.token = access_token
        self.all_images_likes = []
        self.version = version
        self.id = ""
        self.album = "profile"
        self.params = {'access_token': self.token, 'v': self.version}
        self.photos_info = {'photos': []}

    def change_id(self, user_id):
        self.id = user_id

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        if response.status_code != 200:
            print(f"ERROR code: {response.status_code}")
        return response.json()

    def photos_get(self, album):
        self.album = album
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id,
                  "album_id": self.album,
                  "extended": "1"
                  }
        response = requests.get(url, params={**self.params, **params})
        if response.status_code != 200:
            print(f"ERROR code: {response.status_code}")
        return response.json()

    def save_photos(self, album):
        isexits = os.path.exists(f'{album}_{self.id}')
        if not isexits:
            os.mkdir(f'./{album}_{self.id}')
        for image in self.photos_get(album)['response']['items']:
            max_size = 0
            size_type = ""
            likes_count = image['likes']['count']
            if likes_count in self.all_images_likes:
                likes_count = f'{image["likes"]["count"]}_{image["date"]}'
            for size in image['sizes']:
                if size['height'] > max_size:
                    max_size = size['height']
                    photo_url = size['url']
                    size_type = size['type']
            resource = urllib.request.urlopen(photo_url)
            self.photos_info['photos'].append({'file_name': f"{likes_count}.jpg", "type": size_type,
                                               'folder_name': f"{album}_{self.id}"})
            out = open(f"{self.album}_{self.id}/{likes_count}.jpg", 'wb')
            out.write(resource.read())
            out.close()
            self.all_images_likes.append(likes_count)
        with open(f'{self.album}_{self.id}_photos_info.json', 'w+') as f:
            json.dump(self.photos_info, f)
