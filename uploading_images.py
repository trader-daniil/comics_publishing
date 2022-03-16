import os
import random
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def get_comic_url():
    comic_num = random.randint(1, 2500)
    comic_url = f'https://xkcd.com/{comic_num}/info.0.json'
    return comic_url


def get_full_image_path(url, image_name, image_folder):
    """
    return full image path
    """
    image_url = urlparse(url)
    filename, file_extension = os.path.splitext(image_url.path)
    full_image_path = f'{image_folder}/{image_name}{file_extension}'
    return full_image_path


def get_extension(url):
    """
    get image extension from url
    """
    image_url = urlparse(url)
    filename, file_extension = os.path.splitext(image_url.path)

    return file_extension


def parse_image_info(comic_url):
    """
    get comic url
    and author comment from response
    """
    comic_response = requests.get(url=comic_url)
    comic_response.raise_for_status()
    image_url = comic_response.json()['img']
    comment_to_image = comic_response.json()['alt']
    image_info = {
        'image_url': image_url,
        'author_comment': comment_to_image,
    }
    return image_info


def download_image(image_url, image_path):
    """
    get image and
    saving it into folder
    """
    image_response = requests.get(url=image_url)
    with open(image_path, 'wb') as file:
        file.write(image_response.content)


def get_user_groups(vk_token):
    vk_groups_url = 'https://api.vk.com/method/groups.get'
    params = {
        'access_token': vk_token,
        'v': '5.81',
    }
    response = requests.get(
        url=vk_groups_url,
        params=params,
    )
    response.raise_for_status()
    return response.json()


def send_image_to_group(group_id, vk_token):
    """
    send image to your vk group
    """
    vk_wallaper_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': vk_token,
        'group_id': group_id,
        'v': '5.81',
    }
    response = requests.get(
        url=vk_wallaper_url,
        params=params,
    )
    response.raise_for_status()
    upload_url = response.json()['response']['upload_url']
    return upload_url


def send_image_to_wall(image_url, vk_token, image_path):
    """
    sending image to users wall
    """
    params = {
        'access_token': vk_token,
        'v': '5.81',
    }
    with open(image_path, 'rb') as comic:
        files = {'photo': comic}
        response = requests.post(
            url=image_url,
            params=params,
            files=files,
        )
        response.raise_for_status()
    os.remove(image_path)
    return response.json()


def save_image_to_group(image_hash, photo, image_server, vk_token, group_id):
    """
    saving image to the group
    """
    saving_url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token': vk_token,
        'v': '5.81',
        'hash': image_hash,
        'server': image_server,
        'photo': photo,
        'group_id': group_id,
    }
    response = requests.post(
        url=saving_url,
        params=params
    )
    response.raise_for_status()
    return response.json()['response'][0]


def publish_image_on_wall(group_id, message, vk_token, attachments):
    """
    sending image on the group wall
    """
    publish_url = 'https://api.vk.com/method/wall.post'
    params = {
        'access_token': vk_token,
        'v': '5.81',
        'owner_id': '-' + group_id,
        'from_group': 1,
        'message': message,
        'attachments': attachments,
    }
    response = requests.get(
        url=publish_url,
        params=params,
    )
    return response.json()


def main():
    load_dotenv()
    photos_path = os.environ.get(
        'IMAGES_PATH',
        'comics',
    )
    Path(photos_path).mkdir(
        parents=True,
        exist_ok=True,
    )
    comic_url = get_comic_url()
    image_info = parse_image_info(comic_url=comic_url)
    image_url = image_info['image_url']
    author_comment = image_info['author_comment']
    image_name = 'first_comic'
    full_image_path = get_full_image_path(
        url=image_url,
        image_name=image_name,
        image_folder=photos_path,
    )
    download_image(
        image_url=image_url,
        image_path=full_image_path,
    )

    vk_token = os.getenv('VK_ACCESS_TOKEN')
    group_id = os.getenv('VK_GROUP_ID')
    image_url = send_image_to_group(
        group_id=group_id,
        vk_token=vk_token,
    )
    image_info = send_image_to_wall(
        image_url=image_url,
        vk_token=vk_token,
        image_path=full_image_path,
    )
    server = image_info['server']
    photo = image_info['photo']
    image_hash = image_info['hash']
    image_response = save_image_to_group(
        image_hash=image_hash,
        photo=photo,
        image_server=server,
        vk_token=vk_token,
        group_id=group_id,
    )
    owner_id = str(image_response['owner_id'])
    media_id = str(image_response['id'])
    attachments = 'photo' + owner_id + '_' + media_id
    publish_image_on_wall(
        group_id=group_id,
        message=author_comment,
        vk_token=vk_token,
        attachments=attachments,
    )


if __name__ == '__main__':
    main()