from django.contrib import admin
from .models import Receipt, ReceiptHasToy, Delivery


class ReceiptItemInline(admin.TabularInline):
    model = ReceiptHasToy
    raw_id_fields = ['toy']


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'amount', 'date']
    list_filter = ['date', 'status']
    list_editable = ['status']
    inlines = [ReceiptItemInline]


class DeliveryAdmin(admin.ModelAdmin):
    model = Delivery
    list_display = ['id', 'address', 'phone']
    raw_id_fields = ['user']


admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(Receipt, ReceiptAdmin)
