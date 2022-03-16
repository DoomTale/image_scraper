from getimages import ImagesLinks, Images


url_link = input('>')
links = ImagesLinks(url_link)
if links.ping():
    links.get()
    images = Images(url_link, links.links)
    images.download_image()