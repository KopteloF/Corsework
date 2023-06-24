import json
import os
import requests
from datetime import datetime
from tqdm import tqdm
from pprint import pprint
from vk_api import VkApi
from ya_disk_api import YaDiskApi

class PhotoBackup:
    def __init__(self, vk_token, disk_token):
        self.vk_api = VkApi(vk_token)
        self.ya_disk_api = YaDiskApi(disk_token)

    def backup_photos(self, user_id, num_photos):
        photos = self.vk_api.get_photos(user_id, num_photos)
        file_info = []

        self.ya_disk_api.create_folder('/Photos')

        for photo in tqdm(photos):
            max_res_photo = sorted(photo['sizes'], key=lambda x: x['width'] * x['height'], reverse=True)[0]

            likes = photo['likes']['count']

            if any(d['likes'] == likes for d in file_info):
                file_name = f"{likes}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
            else:
                file_name = f"{likes}.jpg"

            photo_url = max_res_photo['url']
            photo_bytes = requests.get(photo_url).content

            file_path = f'/Photos/{file_name}'
            self.ya_disk_api.upload_file(file_path, photo_bytes)

            file_size = len(photo_bytes)
            file_info.append({'file_name': file_name, 'size': file_size, 'likes': likes})

        with open('file_info.json', 'w') as f:
            json.dump(file_info, f)

        pprint(file_info)
        print('Backup complete.')