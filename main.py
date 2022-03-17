from getimages import ImagesFromLinks

url_link = input('>')
links = ImagesFromLinks(url_link)
links.save_images_from_link()
