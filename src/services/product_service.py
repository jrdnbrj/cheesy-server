import base64
import requests

from decouple import config
from ..db.documents import Product


def create_product(**kwargs):
    return Product(**kwargs).save()

def get_products():
    products = Product.objects()

    for product in products:
        product.images[0] = to_base64(product.images[0])
    
    return products

def get_product_by_path(path):
    product = Product.objects(path=path).first()
    product.images = [to_base64(img) for img in product.images]

    return product

def to_base64(img_name):
    try:
        image_url = config('URL') + "static/" + img_name
        image = base64.b64encode(requests.get(image_url).content)
        return image.decode('utf-8')
    except:
        return ''