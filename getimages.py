import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from tqdm import tqdm
import pathlib


class ImagesLinks:
    def __init__(self, url):
        self.links = []
        self.url = url

    def ping(self, url=''):
        """
        Checks if url is a valid URL.
        """
        if url == '':
            url = self.url
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def get(self):
        """
         Get image from scrap
         """
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                found_images = soup.find_all("img")
                for img in tqdm(found_images, "URLs: "):
                    img_url = img.attrs.get("src")
                    if not img_url:
                        continue
                    img_url = urljoin(self.url, img_url)
                    try:
                        pos = img_url.index("?")
                        img_url = img_url[:pos]
                    except ValueError:
                        pass
                    if self.ping(img_url):
                        self.links.append(img_url)
        except (ValueError, Exception):
            print('An exception occurred')


class ImagesFromLinks(ImagesLinks):

    def __get_dir_name(self):
        """
        Get dir name
        """
        parsed = urlparse(self.url)
        line = ''.join(filter(str.isalnum, str(parsed.netloc)))
        str_dir = 'images/' + line
        return str_dir

    def download_images(self):
        """
        Downloads an image
        """
        path_dir = self.__get_dir_name()
        if not os.path.isdir(path_dir):
            os.makedirs(path_dir)
        for img_url in tqdm(self.links, "Saving:"):
            try:
                filename = os.path.join(path_dir, img_url.split('/')[-1])
                file_extension = pathlib.Path(filename).suffix
                if file_extension == "":
                    filename = str(filename) + '.png'
                elif file_extension.lower().endswith(('.png', '.jpg', '.jpeg')):
                    filename = str(filename).replace(file_extension, '.png')
                else:
                    return
                response = requests.get(img_url, stream=True)
                if response.status_code == 200:
                    with open(filename, 'wb') as file:
                        for chunk in response:
                            file.write(chunk)
            except (ValueError, Exception):
                print('An exception occurred')

    def save_images_from_link(self):

        try:
            if self.ping():
                self.get()
                self.download_images()
            else:
                print('Wrong link')
        except (ValueError, Exception):
            print('An exception occurred')
