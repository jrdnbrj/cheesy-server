from ..db.documents import Order


def get_orders():
    return Order.objects()
