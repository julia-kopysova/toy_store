from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from receipt import views as views_checkout

urlpatterns = [
    path('checkout/', views_checkout.create_receipt, name='checkout'),
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
