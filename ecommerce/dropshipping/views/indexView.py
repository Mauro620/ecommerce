from django.shortcuts import render
from dropshipping.models.productModel import Products
from django.db.models import Avg
from django.shortcuts import redirect
from dropshipping.utils import convert_currency
from dropshipping.utils.formatters import round_to_1_decimal
from django.db.models.functions import Round
from dropshipping.services.productService import convert_product

def index(request):
    products = Products.objects.prefetch_related('images').annotate(
        avg_rating=Round(Avg('reviews__rating'), 1)  # Redondear a 1 decimal
)
    selected_currency = request.session.get("currency", "COP")

    for product in products:
        convert_product(request, product)

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
