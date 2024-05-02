from PIL import Image
def resize_image(image, max_width, max_height):
    img = Image.open(image)
    img.thumbnail((max_width, max_height))
    return img