from django.urls import path
from dropshipping import views

urlpatterns = [ 
    path('', views.index, name='home'),
    path('set_currency/', views.set_currency, name='set_currency'),
    path('contact', views.index, name='contact'),
    path('terminos', views.index, name='terms'),
    path('privacy', views.index, name='privacy'),
    path('returns', views.index, name='returns'),
    path('policies', views.index, name='policies'),

    # url pagina del producto
    path('products/<uuid:product_id>', views.detail_product_view, name='product_detail'),
    # path('checkout/<uuid:product_id>/', views.checkout, name='checkout'),
    # url formulario de compra
    # url checkout
    path('checkout/<uuid:product_id>/', views.checkout_step1, name='checkout_step1'),
    path('checkout/<uuid:product_id>/delivery/', views.checkout_step2, name='checkout_step2'),
    path('checkout/<uuid:product_id>/payment/', views.checkout_step3, name='checkout_step3'),
    path('checkout/<uuid:product_id>/complete/', views.checkout_complete, name='checkout_complete'),
    # tu vista del formulario
    path('ajax/load-states/', views.load_states, name='ajax_load_states'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),

    # pasarela de pagos
    #  
] 