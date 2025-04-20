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
