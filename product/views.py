from django.shortcuts import render, redirect, get_object_or_404
from .models import Toy, Type


def toys_list(request, slug=None):
    type_toy = None
    # types_toy = Type.objects.all()
    types_toy = Type.objects.raw("SELECT * FROM product_type")
    # toys = Toy.objects.filter(available=True)
    toys = Toy.objects.raw("SELECT * FROM product_toy WHERE available=%s", [True])
    if slug:
        # type_toy = get_object_or_404(Type, slug=slug)
        type_toy = Type.objects.raw("SELECT * FROM product_type WHERE slug=%s", [slug])[0]
        # toys = toys.filter(type=type_toy)
        toys = Toy.objects.raw("SELECT * FROM product_toy WHERE type_id=%s", [type_toy.id])

    return render(request, 'catalog.html', {'type_toy': type_toy, 'types_toy': types_toy, 'toys': toys})


def toy_detail(request, id):
    # cart_product_form = CartAddProductForm()
    # toy = get_object_or_404(Toy, id=id, available=True)
    toy = Toy.objects.raw("SELECT * FROM product_toy WHERE id=%s AND available=%s", [id, True])[0]
    return render(request, 'detail.html', {'toy': toy})
    # return render(request, 'product.html', {'product': product, 'cart_form': cart_product_form})

