from django.shortcuts import render, redirect, get_object_or_404
from .models import Toy, Type
# from django.views.generic import ListView, DetailView
# from cart.forms import CartAddProductForm


def toys_list(request, slug=None):
    type_toy = None
    types_toy = Type.objects.all()
    toys = Toy.objects.filter(available=True)
    if slug:
        type_toy = get_object_or_404(Type, slug=slug)
        toys = toys.filter(type=type_toy)
    return render(request, 'catalog.html', {'type_toy': type_toy, 'types_toy': types_toy, 'toys': toys})


# def product_detail(request, id):
#     cart_product_form = CartAddProductForm()
#     product = get_object_or_404(Product, id=id, available=True)
#     return render(request, 'product.html', {'product': product, 'cart_form': cart_product_form})

