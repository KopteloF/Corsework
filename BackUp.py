import requests
from tqdm import tqdm
import json
import os
from pprint import pprint
from datetime import datetime

# Внесение идентификатора пользователя, токен VK и токен Ya.Disk
user_id = '...'
vk_token = '...'
disk_token = '...'

# Запрос фотографий из VK API
response = requests.get(f'https://api.vk.com/method/photos.get?owner_id={user_id}&album_id=profile&access_token={vk_token}&v=5.131&extended=1')
photos = response.json()['response']['items']

# Получение информации о фотографии из ответа VK API
file_info = []

# Создание каталог на Ya.Disk для фотографий, если он еще не существует.
url = 'https://cloud-api.yandex.net/v1/disk/resources'
headers = {'Authorization': f'OAuth {disk_token}'}
params = {'path': '/Photos', 'overwrite': 'false'}
response = requests.put(url, headers=headers, params=params)

if response.status_code == 201:
    print('Created directory on Ya.Disk')

# Запрос количества загружаемых пользователем фото
num_photos = input("Введите количество загружаемых фотографий (или введите 'all' для загрузки всех фото): ")

# Если пользователь вводит 'all', то загружаются все доступные фотографии
if num_photos == 'all':
    num_photos = len(photos)
# В противном случае загружается указанное количество фотографий
# Если введенное число выше числа фотографий, произойдет скачивание всех фотографий
else:
    num_photos = int(num_photos)

for photo in tqdm(photos[:num_photos]):
    # Получение фотографий с наивысшим разрешением
    max_res_photo = sorted(photo['sizes'], key=lambda x: x['width'] * x['height'], reverse=True)[0]

    # Получение количества лайков
    likes = photo['likes']['count']

    # Проверка на совпадение количества лайков
    if any(d['likes'] == likes for d in file_info):
        file_name = f"{likes}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
    else:
        file_name = f"{likes}.jpg"

    # Скачивание фото из VK
    photo_url = max_res_photo['url']
    photo_bytes = requests.get(photo_url).content

    # Загрузка фото на Ya.Disk в созданную директорию
    url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {disk_token}'}
    params = {'path': f'/Photos/{file_name}', 'overwrite': 'false'}
    response = requests.get(url, headers=headers, params=params).json()

    if 'href' not in response:
        print(f"Could not retrieve upload URL for {file_name}")
        continue

    upload_url = response['href']
    upload_response = requests.put(upload_url, data=photo_bytes)

    if upload_response.status_code != 201:
        print(f"Failed to upload {file_name} to Yandex.Disk")
        continue

    # Добавление информации о файле в список
    file_size = len(photo_bytes)
    file_info.append({'file_name': file_name, 'size': file_size, 'likes': likes})

# Сохранение информации о файле в json-файл
with open('file_info.json', 'w') as f:
    json.dump(file_info, f)

# Отображение информации о файле
print(json.dumps(file_info, indent=2))

# Отображение сообщения о завершении
print('Backup complete.')