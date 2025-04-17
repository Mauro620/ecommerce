from django.contrib import admin
from .models import Users, Products, Orders, OrderDetail, Payments, Review, Image

# Registrar cada modelo
admin.site.register(Users)
admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(OrderDetail)
admin.site.register(Payments)
admin.site.register(Review)
admin.site.register(Image)