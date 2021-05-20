from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('account/', views.own_account, name='account'),
    # path('account/edit_account', views.edit_account, name='edit_account'),
    path('account/change_password', views.change_password, name='change_password'),
]