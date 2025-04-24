from dropshipping.models.reviewsModel import Review
from dropshipping.models.ordersModel import Orders
from dropshipping.models.ordersDetailModel import OrderDetail
from dropshipping.models.userModel import Users
from django.core.exceptions import ValidationError

class ReviewService:
    @staticmethod
    def user_can_review(user, product_id):
        return OrderDetail.objects.filter(
            order__user=user,
            product=product_id,
        ).exists()

    @staticmethod
    def create_review(product, form):
        email = form.cleaned_data['email']
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            raise ValidationError("No se encontró un usuario con este email.")

        if not ReviewService.user_can_review(user, product.product_id):
            raise ValidationError("Solo los compradores pueden dejar reseñas.")

        review = form.save(commit=False)
        review.user = user
        review.product = product
        review.save()
        return review
    
    @staticmethod
    def get_review_value(product):
        reviews = Review.objects.filter(product=product)
        if not reviews.exists():
            return 0
        total_rating = sum(review.rating for review in reviews)
        values = { 
            5: 0,
            4: 0,
            3: 0,
            2: 0,
            1: 0
        }
        for review in reviews:
            if review.rating not in values:
                raise ValidationError("Valor de reseña no válido.")
            values[review.rating] += 1
        for value in values:
            values[value] = round((values[value] / len(reviews)) * 100)


        return values
