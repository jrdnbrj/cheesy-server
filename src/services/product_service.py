import base64
import requests

from decouple import config
from ..db.documents import Product


def edit_product(**kwargs):
    path = kwargs.get('path', 'nada')
    try:
        product = Product.objects(path=path).update(**kwargs)
        return True
    except:
        return False

def get_products():
    products = Product.objects()

    for product in products:
        # product.images[0] = config('URL') + "static/" + product.images[0]
        product.images = [config('URL') + "static/" + img for img in product.images]
    
    return products

def get_product_by_path(path):
    product = Product.objects(path=path).first()
    product.images = [config('URL') + "static/" + img for img in product.images]
    # product.images = [to_base64(img) for img in product.images]

    return product

def to_base64(img_name):
    try:
        image_url = config('URL') + "static/" + img_name
        image = base64.b64encode(requests.get(image_url).content)
        return image.decode('utf-8')
    except:
        return ''