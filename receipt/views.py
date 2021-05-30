import logging
import logging.config
import sys

from django.shortcuts import render, get_object_or_404

from cart.cart import Cart
from product.models import Toy
from .forms import DeliveryForm
from .models import Receipt, ReceiptHasToy, Delivery

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


def create_receipt(request):
    form = DeliveryForm(request.POST)
    logging.info(form)
    user = request.user
    cart = Cart(request)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            delivery = Delivery(user=user, address=cd['address'], phone=cd['phone'])
            delivery.save()
            total_price = cart.get_total_price()
            created_receipt = Receipt(user=user, delivery=delivery, amount=total_price)
            created_receipt.save()
            for position in cart:
                receipt_has_toy = ReceiptHasToy.objects.create(receipt=created_receipt, toy=position['product'],
                                                               price=position['price'],
                                                               count=position['quantity'])
                product = position['product']
                our_product = get_object_or_404(Toy, id=product.id)
                if position['quantity'] < our_product.count:
                    our_product.count = our_product.count - position['quantity']
                else:
                    our_product.available = False
                    our_product.count = 1
                our_product.save()
            cart.clear()
            return render(request, 'returned_receipt.html', {'order': created_receipt})
        else:
            form = DeliveryForm(request.POST)
    return render(request, 'checkout.html', {'form': form})

# def display_info(request):
# user = request.user
# o = get_object_or_404(Order, user = user)
# return render(request,'success.html', { 'order': o })
