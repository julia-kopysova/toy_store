import logging
import logging.config
import sys

from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from product.models import Toy
from .cart import Cart
from .forms import CartAddProductForm

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


@require_POST
def cart_add(request, id):
    cart = Cart(request)
    logging.info(cart)
    # toy = get_object_or_404(Toy, id=id)
    toy = Toy.objects.raw("SELECT * FROM product_toy WHERE id = %s", [id])[0]
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(toy=toy, quantity=cd['quantity'], update_quantity=cd['update'])
        toy_id = str(toy.id)
        if cart.cart[toy_id]['quantity'] > toy.count:
            cart.cart[toy_id]['quantity'] = toy.count
    return redirect('cart')


def cart_remove(request, id):
    cart = Cart(request)
    # toy = get_object_or_404(Toy, id=id)
    toy = Toy.objects.raw("SELECT * FROM product_toy WHERE id = %s", [id])[0]
    cart.remove(toy)
    return redirect('cart')


def remove_all_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart')


def cart_display(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
        logging.info(item['update_quantity_form'])
    return render(request, 'cart.html', {'cart': cart})
