from datetime import datetime
import base64

from decouple import config
from ..db.documents import Product


def get_products():
    products = Product.objects().order_by('sequence')

    for product in products:
        product.images = [config('URL') + "static/" + img for img in product.images]

        for smoothie in product.smoothies:
            smoothie[1] = config('URL') + "static/" + smoothie[1]
    
    return products


def edit_product(**kwargs):
    try:
        path = kwargs.get('path')

        images = []
        for image in kwargs.get('images'):
            if '/static/' not in image:
                img = image.split('base64,')[1]
                filename = base64_to_file(img)
            else:
                filename = image.split('/')[-1]

            images.append(filename)

        smoothies = []
        for smoothie in kwargs.get('smoothies'):
            if '/static/' not in smoothie[1]:
                img = smoothie[1].split('base64,')[1]
                smoothie[1] = base64_to_file(img) 
            else:
                smoothie[1] = smoothie[1].split('/')[-1] 
                
            smoothies.append(smoothie)

        kwargs['images'] = images
        kwargs['smoothies'] = smoothies

        Product.objects(path=path).update(**kwargs)

        return True
        
    except:
        return False


def get_product_by_path(path):
    product = Product.objects(path=path).first()
    product.images = [config('URL') + "static/" + img for img in product.images]

    for smoothie in product.smoothies:
        smoothie[1] = config('URL') + "static/" + smoothie[1]

    return product


def base64_to_file(img_encoded):
    img = base64.b64decode(img_encoded)
    filename = str(datetime.now()) + '.png'
    with open('static/' + filename, 'wb') as file:
        file.write(img)
    
    return filename
