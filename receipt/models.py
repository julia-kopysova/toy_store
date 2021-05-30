from django.db import models
from django.conf import settings
from product.models import Toy
from phone_field import PhoneField


class Delivery(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = PhoneField(blank=False, null=False, help_text='Contact phone number')
    address = models.CharField(max_length=200, blank=False, null=False)


class Receipt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    toys = models.ManyToManyField(Toy, through="ReceiptHasToy", blank=False, null=False)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    STATUS_CHOICES = (
        ('Accepted', 'Accepted'),
        ('Contacted', 'Contacted'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=9, default='Accepted', blank=False, null=False)


class ReceiptHasToy(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    toy = models.ForeignKey(Toy, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.price * self.count
