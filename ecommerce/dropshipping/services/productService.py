# services/product_service.py
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from dropshipping.models.productModel import Products
from dropshipping.utils.exchanges import convert_currency



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

def convert_product(request, product):
    selected_currency = request.session.get("currency", "COP")
    converted_price = convert_currency(product.end_price, "COP", selected_currency)
    converted_offer_price = convert_currency(product.offer_price, "COP", selected_currency)

    if selected_currency == "COP" or selected_currency == "ARS" or selected_currency == "CLP":
        product.converted_price = round(converted_price)
        product.converted_offer_price = round(converted_offer_price)
        product.currency = selected_currency
        return product
    
    product.converted_price = round(converted_price, 2)
    product.converted_offer_price = round(converted_offer_price, 2)
    product.currency = selected_currency

    return product