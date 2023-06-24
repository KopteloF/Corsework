import requests

class YaDiskApi:
    def __init__(self, disk_token):
        self.disk_token = disk_token
        self.url_prefix = 'https://cloud-api.yandex.net/v1/disk/resources'

    def create_folder(self, folder_path):
        headers = {'Authorization': f'OAuth {self.disk_token}'}
        params = {'path': folder_path, 'overwrite': 'false'}
        response = requests.put(self.url_prefix, headers=headers, params=params)

        if response.status_code == 201:
            print(f'Created {folder_path} directory on Ya.Disk')

    def upload_file(self, file_path, file_bytes):
        url = f'{self.url_prefix}/upload'
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.disk_token}'}
        params = {'path': file_path, 'overwrite': 'false'}
        response = requests.get(url, headers=headers, params=params).json()

        if 'href' not in response:
            print(f"Could not retrieve upload URL for {file_path}")
            return

        upload_url = response['href']
        upload_response = requests.put(upload_url, data=file_bytes)

        if upload_response.status_code != 201:
            print(f"Failed to upload {file_path} to Yandex.Disk")
            return

        print(f"Uploaded {file_path} to Yandex.Disk")