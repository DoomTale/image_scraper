import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from tqdm import tqdm
import pathlib


def __link_is_valid(url_link):
    """
    Checks if url is a valid URL.
    """
    parsed = urlparse(url_link)
    return bool(parsed.netloc) and bool(parsed.scheme)


def __get_all_images_links(url_link):
    """
    Get image from scrap with passing 403
    """
    response = requests.get(url_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        img_urls = []
        found_images = soup.find_all("img")
        for img in tqdm(found_images, "URLs: "):
            img_url = img.attrs.get("src")
            if not img_url:
                continue
            img_url = urljoin(url_link, img_url)
            try:
                pos = img_url.index("?")
                img_url = img_url[:pos]
            except ValueError:
                pass
            if __link_is_valid(img_url):
                img_urls.append(img_url)
        return img_urls


def __get_dir_name(url_link):
    """
    Get dir name
    """
    parsed = urlparse(url_link)
    line = ''.join(filter(str.isalnum, str(parsed.netloc)))
    str_dir = 'images/' + line
    return str_dir


def __download_image(img_url, path_dir):
    """
    Downloads an image
    """
    if not os.path.isdir(path_dir):
        os.makedirs(path_dir)
    filename = os.path.join(path_dir, img_url.split('/')[-1])
    file_extension = pathlib.Path(filename).suffix
    if file_extension == "":
        filename = str(filename) + '.png'
    elif file_extension.lower().endswith(('.png', '.jpg', '.jpeg')):
        filename = str(filename).replace(file_extension, '.png')
    else:
        return
    try:
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                for chunk in response:
                    file.write(chunk)
    except:
         print("An exception occurred")


def get_images(url_link):
    if __link_is_valid(url_link):
        img_list = __get_all_images_links(url_link)
        path_dir = __get_dir_name(url_link)
        for img_item in tqdm(img_list, "Saving:"):
            __download_image(img_item, path_dir)
