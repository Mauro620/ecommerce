from django.db import models
import uuid
from django.db.models import Avg

class Products(models.Model):
    product_id = models.UUIDField(default=uuid.uuid4 , primary_key=True)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True)
    price_base = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    end_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    stock = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    @property
    def average_rating(self):
        return self.reviews.objects.filter(product=self).aggregate(Avg('rating'))['rating__avg'] or 0   
    
    @property
    def review_count(self):
        return self.reviews.count()

