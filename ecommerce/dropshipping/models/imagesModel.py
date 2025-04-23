from django.db import models
from .productModel import Products
from django.conf import settings
from django.templatetags.static import static
import os

class Image(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/images/')  # Se guardará en media/products/images/
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Imagen de {self.product.name}"
    
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url') and os.path.exists(self.image.path):
            return self.image.url
        return None