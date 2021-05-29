from django import forms


class DeliveryForm(forms.Form):
    phone = forms.CharField(max_length=200)
    address = forms.CharField(max_length=200)