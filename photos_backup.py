import json
import requests
import urllib.request
import os

access_token_vk = 'vk1.a.RQ0L9ImzVUBLnJ0jvDsnMgW1EjZlyBGHghvBXiBKpXtkYctv4X_UJBTnvasVrDGrsl1lPQrIAP-budDn4RsPYS2XhvrHwp8pgtoDmCxIizRHVuaXeEf-UoImbAwBr3mlMl_z5JkjPdvruCUyFO51GK8dU2KPvUKA0CQ16cppnhvA3Lvo7nJ_rX0V12cJ8j224LOiUJT1NoMmoha7ommtWA'


class VK:

    def __init__(self, access_token, version='5.131'):
        self.token = access_token
        self.all_images_likes = []
        self.version = version
        self.id = ""
        self.album = "profile"
        self.yandex_token = ""
        self.params = {'access_token': self.token, 'v': self.version}
        self.photos_info = {'photos': []}

    def change_id(self,user_id):
        self.id = user_id

    def change_token(self,token):
        self.yandex_token = token

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def photos_get(self,album):
        self.album = album
        url = 'https://api.vk.com/method/photos.get'
        params={'owner_id': self.id,
                "album_id": album,
                "extended": "1"
                }
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def save_photos(self,album):
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
            self.photos_info['photos'].append({'file_name': f"{album}_{self.id}/{likes_count}.jpg","type":size_type})
            out = open(f"{self.album}_{self.id}/{likes_count}.jpg", 'wb')
            out.write(resource.read())
            out.close()
            self.all_images_likes.append(likes_count)
        with open(f'{self.album}_{self.id}_photos_info.json', 'w+') as f:
            json.dump(self.photos_info, f)

    def yandex_photo(self,img_path):
        headers = {'Authorization': self.yandex_token}
        params = {'path': f"{img_path}"}
        requests.put('https://cloud-api.yandex.net/v1/disk/resources', params={'path': f'{self.album}_{self.id}'}, headers=headers)
        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', params=params, headers=headers)
        if response.status_code in range(200, 300):
            with open(img_path, "rb") as file:
                response = requests.put(response.json()['href'], file)
            return response.status_code
        elif response.status_code == 409:
            return response.status_code

    def send_photo_yandex(self, amount=5):
        sent_photos = 0
        for file_name in self.photos_info['photos']:
            if sent_photos == amount:
                print("photos successfully uploaded")
                break
            status_code = self.yandex_photo(file_name['file_name'])
            if status_code in range(200, 300):
                sent_photos += 1
                print(f'number of sent photos: {sent_photos} out of {amount}')
            if len(self.photos_info['photos']) == self.how_many_items():
                print("all your photos have been successfully uploaded to Yandex disk")
                break

    def how_many_items(self):
        headers = {'Authorization': self.yandex_token}
        params = {'path': f"{self.album}_{self.id}/"}
        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources', params=params, headers=headers)
        return len(response.json()['_embedded']['items'])

access_token_vk = 'vk1.a.RQ0L9ImzVUBLnJ0jvDsnMgW1EjZlyBGHghvBXiBKpXtkYctv4X_UJBTnvasVrDGrsl1lPQrIAP-budDn4RsPYS2XhvrHwp8pgtoDmCxIizRHVuaXeEf-UoImbAwBr3mlMl_z5JkjPdvruCUyFO51GK8dU2KPvUKA0CQ16cppnhvA3Lvo7nJ_rX0V12cJ8j224LOiUJT1NoMmoha7ommtWA'
vk = VK(access_token_vk)

while True:
    print("This program save your VK photos to Yandex disk")
    if vk.id == "":
        user_id = input("enter your vk id: ")
        vk.change_id(user_id)
    if vk.yandex_token == "":
        yandex_token = input("enter your yandex disk token: ")
        vk.change_token(yandex_token)
    while True:
        print("Select option:\n1.Save photos from VK\n2.Load photos to Yandex disk\n"
              "3.Change user id\n4.Change Yandex disk token\n5.Exit\n")
        selected_option = input()
        if selected_option == "1":
            album = input("Choose album\n1.profile\n2.wall\n")
            if album == '1':
                vk.save_photos('profile')
            elif album == '2':
                vk.save_photos('wall')
            else:
                print("No such option")
        elif selected_option == "2":
            if not vk.photos_info['photos']:
                vk.save_photos('profile')
            vk.send_photo_yandex(int(input("enter the number of photos\n")))
        elif selected_option == "3":
            vk.change_id(input("enter new vk id"))
        elif selected_option == "4":
            vk.change_token(input("enter new Yandex disk token"))
        elif selected_option == "5":
            quit()
        else:
            print("No such option")