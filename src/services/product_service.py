from datetime import datetime
import base64
import requests

from decouple import config
from ..db.documents import Product


def edit_product(**kwargs):
    try:
        path = kwargs.get('path', 'nada')
        images = []
        for image in kwargs.get('images'):
            if 'static' not in image:
                img = image.split('base64,')[1]
                img = base64.b64decode(img)
                filename = str(datetime.now()) + '.png'
                with open('static/' + filename, 'wb') as file:
                    file.write(img)
                images.append(filename)
            else:
                name = image.split('/')[-1]
                images.append(name)

        kwargs['images'] = images
        Product.objects(path=path).update(**kwargs)
        return True
        
    except:
        return False

def get_products():
    products = Product.objects().order_by('sequence')

    for product in products:
        product.images = [config('URL') + "static/" + img for img in product.images]
    
    return products

def get_product_by_path(path):
    product = Product.objects(path=path).first()
    product.images = [config('URL') + "static/" + img for img in product.images]

    return product

# def to_base64(img_name):
#     try:
#         image_url = config('URL') + "static/" + img_name
#         image = base64.b64encode(requests.get(image_url).content)
#         return image.decode('utf-8')
#     except:
#         return ''