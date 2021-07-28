from ..db.documents import Order


def get_orders():
    orders = Order.objects()
    print('Orders:', orders[0])
    print('Type:', orders[0].type)
    print('Square:', orders[0].square.status)
    return orders
