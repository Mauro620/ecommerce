from django.db import models
import uuid
from .productModel import Products
from .userModel import Users

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, null=False, on_delete=models.CASCADE)
    rating = models.IntegerField(null=False)
    comment = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.id} for Product {self.product_id}"