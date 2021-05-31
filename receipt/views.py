import logging
import logging.config
import sys
from datetime import datetime
from django.utils import timezone
# from django.utils.timezone import pytz, now

from django.db import connection
from django.shortcuts import render, redirect

from cart.cart import Cart
from product.models import Toy
from toy_store import settings
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
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO receipt_delivery(user_id, address, phone) "
                               "VALUES (%s , %s, %s)", [user.id, cd['address'], cd['phone']])
                id_delivery = cursor.lastrowid
                logging.info(id_delivery)
            total_price = cart.get_total_price()
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO receipt_receipt(user_id, date, delivery_id, amount, status) "
                               "VALUES (%s, %s, %s, %s, %s)",
                               [user.id, timezone.now(), id_delivery, total_price,
                                "Accepted"])
                id_receipt = cursor.lastrowid
                logging.info(id_receipt)
            for position in cart:
                product = position['product']
                our_product = Toy.objects.raw("SELECT * FROM product_toy WHERE id=%s", [product.id])[0]
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO receipt_receipthastoy(receipt_id, toy_id, "
                                   "price, count) VALUES (%s, %s, %s, %s)", [id_receipt, our_product.id,
                                                                             position['price'], position['quantity']])
                if position['quantity'] < our_product.count:
                    our_product.count = our_product.count - position['quantity']
                else:
                    our_product.available = False
                    our_product.count = 1
                our_product.save()
            cart.clear()
            return render(request, 'returned_receipt.html', {'order': id_receipt})
        else:
            form = DeliveryForm(request.POST)
    return render(request, 'checkout.html', {'form': form})


# def cancel_receipt(request, id):
#     with connection.cursor() as cursor:
#         cursor.execute("UPDATE receipt_receipt SET status = %s WHERE id = %s", ["Canceled", id])
#         cursor.execute("UPDATE product_toy SET status = %s WHERE id = %s", ["Canceled", id])
#     return redirect('account')

# def display_info(request):
# user = request.user
# o = get_object_or_404(Order, user = user)
# return render(request,'success.html', { 'order': o })
