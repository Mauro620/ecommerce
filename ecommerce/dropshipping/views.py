# dropshipping/views.py
from .views.indexView import index
from .views.productView import detail_product_view as detailProduct
from .views.checkoutView import (
    checkout_step1,
    checkout_step2,
    checkout_step3,
    checkout_complete,
)
