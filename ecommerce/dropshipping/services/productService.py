# services/product_service.py
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from dropshipping.models.productModel import Products



def get_product_with_reviews(product_id):
    product = get_object_or_404(
        Products.objects.prefetch_related('images', 'reviews__user').all(),
        product_id=product_id
    )
    return product

def get_product_reviews_data(product):
    reviews = product.reviews.all().order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    rating_count = reviews.count()
    return {
        "reviews": reviews,
        "rating_avg": avg_rating,
        "rating_count": rating_count
    }
