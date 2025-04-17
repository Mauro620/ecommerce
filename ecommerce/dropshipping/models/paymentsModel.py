from django.db import models
from .ordersModel import Orders
import uuid

class Payments(models.Model):
    payment_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, null=False)

    def __str__(self):
        return f"Payment {self.payment_id} for Order {self.order.order_id}"
    