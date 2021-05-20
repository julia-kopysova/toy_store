from django.db import models
from django.shortcuts import reverse


class Type(models.Model):
    name = models.CharField(max_length=20, db_index=True, blank=False)
    slug = models.SlugField(max_length=10, db_index=True, unique=True)

    class Meta:
        ordering = ['name', ]
        verbose_name = 'type'
        verbose_name_plural = 'types'

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=20, db_index=True, blank=False)


class Toy(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=False)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, blank=False)
    name = models.CharField(max_length=100, db_index=True, blank=False)
    description = models.TextField(blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    slug = models.SlugField(max_length=10, db_index=True, blank=False)
    color = models.CharField(max_length=20, db_index=True, blank=False)
    size = models.CharField(max_length=20, db_index=True, blank=False)
    image = models.ImageField(upload_to='photo_products', blank=False)
    count = models.PositiveIntegerField(blank=False)
    available = models.BooleanField(default=True, blank=False)
    created = models.DateTimeField(auto_now_add=True, blank=False)

    class Meta:
        ordering = ['name', ]
        index_together = [['id', 'slug'], ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('toy', args=[self.id])
