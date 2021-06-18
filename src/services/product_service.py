import base64
import requests

from decouple import config
from ..db.documents import Product


def create_product(**kwargs):
    return Product(**kwargs).save()

def get_products():
    return Product.objects()

def get_product_by_path(path):
    product = Product.objects(path=path).first()
    
    images = []
    for img in product.images:
        try:
            image_name = config('URL') + "static/" + img
            image = base64.b64encode(requests.get(image_name).content)
            images.append(image.decode('utf-8'))
        except: pass

    product.images = images

    return product
