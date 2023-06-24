import requests

class VkApi:
    def __init__(self, vk_token):
        self.vk_token = vk_token

    def get_photos(self, user_id, num_photos):
        response = requests.get(f'https://api.vk.com/method/photos.get?owner_id={user_id}&album_id=profile&access_token={self.vk_token}&v=5.131&extended=1')
        photos = response.json()['response']['items']

        if num_photos == 'all':
            num_photos = len(photos)
        else:
            num_photos = int(num_photos)
            
        return photos[:num_photos]