from django.db import models
from .userModel import Users
import uuid

class Orders(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    order_status = models.CharField(
        max_length=20, 
        null=False, 
        choices=ORDER_STATUS_CHOICES,
        default='pending'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    order_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.name}"