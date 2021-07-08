from datetime import datetime
import base64
import requests

from decouple import config
from ..db.documents import Product


def edit_product(**kwargs):
    try:
        path = kwargs.get('path')

        images = []
        for image in kwargs.get('images'):
            if '/static/' not in image:
                img = image.split('base64,')[1]
                img = base64.b64decode(img)
                filename = str(datetime.now()) + '.png'
                with open('static/' + filename, 'wb') as file:
                    file.write(img)
                images.append(filename)
            else:
                name = image.split('/')[-1]
                images.append(name)

        smoothies = []
        for smoothie in kwargs.get('smoothies'):
            if '/static/' not in smoothie[1]:
                img = smoothie[1].split('base64,')[1]
                img = base64.b64decode(img)
                filename = str(datetime.now()) + '.png'
                with open('static/' + filename, 'wb') as file:
                    file.write(img)
                smoothies.append([smoothie[0], filename, smoothie[2]])
            else:
                name = smoothie[1].split('/')[-1]
                smoothies.append([smoothie[0], name, smoothie[2]])

        kwargs['images'] = images
        kwargs['smoothies'] = smoothies

        Product.objects(path=path).update(**kwargs)

        return True
        
    except:
        return False

def get_products():
    products = Product.objects().order_by('sequence')

    for product in products:
        product.images = [config('URL') + "static/" + img for img in product.images]

        for smoothie in product.smoothies:
            smoothie[1] = config('URL') + "static/" + smoothie[1]
    
    return products

def get_product_by_path(path):
    product = Product.objects(path=path).first()
    product.images = [config('URL') + "static/" + img for img in product.images]

    for smoothie in product.smoothies:
        smoothie[1] = config('URL') + "static/" + smoothie[1]

    return product

# def to_base64(img_name):
#     try:
#         image_url = config('URL') + "static/" + img_name
#         image = base64.b64encode(requests.get(image_url).content)
#         return image.decode('utf-8')
#     except:
#         return ''