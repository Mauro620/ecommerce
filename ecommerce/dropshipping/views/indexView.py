from django.shortcuts import render
from dropshipping.models.productModel import Products
from django.db.models import Avg
from django.shortcuts import redirect
from dropshipping.utils import convert_currency
from dropshipping.utils.formatters import round_to_1_decimal
from django.db.models.functions import Round

def index(request):
    products = Products.objects.prefetch_related('images').annotate(
        avg_rating=Round(Avg('reviews__rating'), 1)  # Redondear a 1 decimal
)
    selected_currency = request.session.get("currency", "COP")

    for product in products:
        original_price = product.end_price 
        converted_price = convert_currency(original_price, "COP", selected_currency)
        converted_offer_price = convert_currency(product.offer_price, "COP", selected_currency)
        product.converted_offer_price = round(converted_offer_price, 2)
        product.converted_price = round(converted_price, 2)
        product.currency = selected_currency

    for product in products:
        product.image_pairs = [
            product.images.all()[i:i+2] for i in range(0, product.images.count(), 2)
        ]

    context = {
        "title": "shingy",
        "products": products,
        "rating_range": range(1, 6),
    }
    return render(request, 'index.html', context)


def set_currency(request):
    if request.method == "POST":
        currency = request.POST.get("currency", "COP")
        request.session["currency"] = currency
    return redirect(request.META.get("HTTP_REFERER", "/"))
