from django.db import models
from .productModel import Products 
from .ordersModel import Orders
from .addressModel import Address
import uuid

class OrderDetail(models.Model):
    order_detail_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='order_details')
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    address_delivery = models.ForeignKey(Address, max_length=255, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"OrderDetail {self.order_detail_id} for Order {self.order.order_id}"