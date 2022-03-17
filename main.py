from getimages import GetImages

url_link = input('>')
links = GetImages(url_link)
links.save_images_from_link()
