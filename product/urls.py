from django.urls import path,include
from django.conf.urls.static import static
from . import views as v
from django.views.generic.base import TemplateView
from django.conf import settings
#from cart import views as views_cart
#from checkout import views as views_checkout
# from account import views as v_a

urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
    path('catalog/', v.toys_list, name='catalog'),
    path('catalog/<slug>', v.toys_list, name='filter'),
    # path('product/<id>', v.product_detail, name='product'),
    # path('', v.HomeView.as_view(), name='home'),
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
