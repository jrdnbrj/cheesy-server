from ..db.documents import Product

def create_product(**kwargs):
    return Product(**kwargs).save()

def get_products():
    return Product.objects()

def get_product(id):
    return Product.objects(id=id).first()
