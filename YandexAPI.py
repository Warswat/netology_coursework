import requests


class YandexDisk:

    def __init__(self):
        self.yandex_token = ""
        self.folder = ""

    def change_token(self, token):
        self.yandex_token = token

    def yandex_photo(self, img, folder):
        headers = {'Authorization': self.yandex_token}
        params = {'path': f"{self.folder}/{img}"}
        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources', params={'path': f"{self.folder}/"}, headers=headers)
        if response.status_code == 404:
            print("Such folder does not exist, it will be created")
            response = requests.put('https://cloud-api.yandex.net/v1/disk/resources', params={'path': f'{self.folder}'}, headers=headers)
            if response.status_code not in range(200, 300):
                print(f"ERROR, while creating new folder, code: {response.status_code}")
        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', params=params, headers=headers)
        if response.status_code in range(200, 300):
            with open(f"{folder}/{img}", "rb") as file:
                response = requests.put(response.json()['href'], file)
            return response.status_code
        elif response.status_code == 409:
            return response.status_code
        else:
            print(f"ERROR, while get URL for upload, code: {response.status_code}")

    def send_photo_yandex(self, folder, photo_info, amount=5):
        sent_photos = 0
        if len(photo_info['photos']) < amount:
            print(f"Not enough photo {len(photo_info['photos'])} photos will be uploaded")
            amount = len(photo_info['photos'])
        self.folder = folder
        for file_name in photo_info['photos']:
            if sent_photos == amount:
                print("photos successfully uploaded")
                break
            status_code = self.yandex_photo(file_name['file_name'], file_name['folder_name'])
            if status_code in range(200, 300):
                sent_photos += 1
                print(f"number of sent photos: {sent_photos} out of {amount}")
            if len(photo_info['photos']) == self.how_many_items():
                print("all your photos have been successfully uploaded to Yandex disk")
                break

    def how_many_items(self):
        headers = {'Authorization': self.yandex_token}
        params = {'path': f"{self.folder}/"}
        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources', params=params, headers=headers)
        if response.status_code not in range(200, 300):
            print(f"ERROR when receiving data, code : {response.status_code}")
        return len(response.json()['_embedded']['items'])
