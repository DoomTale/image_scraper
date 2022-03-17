from getimages import GetImages

url_link = input('>')
links = GetImages(url_link)
if links.ping():
    links.get()
    links.download_images()
else:
    print('Wrong link')
