# views/product_views.py
from django.shortcuts import render
from dropshipping.services.productService import (
    get_product_with_reviews,
    get_product_reviews_data
)
from dropshipping.utils.formatters import round_to_1_decimal
from dropshipping.utils.exchanges import convert_currency
from dropshipping.forms.formReview import ReviewForm
from dropshipping.services.reviewService import ReviewService
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from dropshipping.services.productService import convert_product


def detail_product_view(request, product_id):
    product = get_product_with_reviews(product_id)
    review_data = get_product_reviews_data(product)

    product_convert = convert_product(request, product)

    review_form = ReviewForm()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            try:
                ReviewService.create_review(product, review_form)
                return redirect('product_detail', product_id=product_convert.product_id)
            except ValidationError as e:
                review_form.add_error(None, e.message)
    context = {
        "product": product_convert,
        "reviews": review_data["reviews"],
        "rating_avg": round_to_1_decimal(review_data["rating_avg"]),
        "rating_count": review_data["rating_count"],
        "rating_range": range(1, 6),
        "rating_range_reverse": range(6, 1, -1),
        "review_form": review_form,
        "unit_review_value": ReviewService.get_review_value(product),
    }
    return render(request, 'products/detail.html', context)

def test_review_product(request, product_id):
    product = get_product_with_reviews(product_id)
    review_data = ReviewService.get_review_value(product)
    context = {
        "product": product,
        "reviews": review_data,
    }
    return render(request, 'products/test_review.html', context)
