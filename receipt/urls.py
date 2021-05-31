from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from receipt import views as views_receipt

urlpatterns = [
    path('checkout/', views_receipt.create_receipt, name='checkout'),
    # path('cancel/<id>', views_receipt.cancel_receipt, name='cancel'),
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
