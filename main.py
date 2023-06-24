from photo_backup import PhotoBackup

user_id = '...'
vk_token = '...'
disk_token = '...'
num_photos = input("Enter the number of photos to upload (or enter 'all' to upload all photos): ")
photo_backup = PhotoBackup(vk_token, disk_token)
photo_backup.backup_photos(user_id, num_photos)