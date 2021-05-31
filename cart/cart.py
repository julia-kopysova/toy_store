import logging
import sys
from decimal import Decimal
from django.conf import settings
from product.models import Toy


LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}
logging.config.dictConfig(LOGGING)


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        logging.info(type(self.cart))
        logging.info(type(self.session))

    def add(self, toy, quantity=1, update_quantity=False):
        toy_id = str(toy.id)
        if toy_id not in self.cart:
            self.cart[toy_id] = {
                'quantity': 0,
                'price': str(toy.price), }
        if update_quantity:
            self.cart[toy_id]['quantity'] = quantity
        else:
            self.cart[toy_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, toy):
        toy_id = str(toy.id)
        if toy_id in self.cart:
            del self.cart[toy_id]
            self.save()

    def amount(self):
        return len(self.cart)

    def __iter__(self):
        # For iteration
        toy_ids = self.cart.keys()
        toys = Toy.objects.filter(id__in=toy_ids)
        for toy in toys:
            self.cart[str(toy.id)]['product'] = toy
        for i in self.cart.values():
            i['price'] = Decimal(i['price'])
            i['total_price'] = i['price'] * i['quantity']
            yield i

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def empty(self):
        if not bool(self.cart):
            return True
        else:
            return False
