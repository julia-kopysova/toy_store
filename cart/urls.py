from django.urls import path
from django.conf.urls.static import static
from . import views as v
from django.conf import settings
from cart import views as views_cart

urlpatterns = [
    path('my_cart/', views_cart.cart_display, name='cart'),
    path('add/<id>', v.cart_add, name='add'),
    path('remove/<id>', v.cart_remove, name='remove'),
    path('delete_all/', v.remove_all_cart, name='delete_all'),
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
