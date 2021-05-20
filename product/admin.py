from django.contrib import admin
from .models import Toy, Material, Type


class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


admin.site.register(Type, TypeAdmin)


class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


admin.site.register(Material, MaterialAdmin)


class ToyAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'count', 'available', 'created', 'color', 'size', 'description', 'type',
                    'material']
    list_filter = ['available', 'name']
    prepopulated_fields = {'slug': ['name', ]}


admin.site.register(Toy, ToyAdmin)
