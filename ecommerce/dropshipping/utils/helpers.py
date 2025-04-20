# utils/helpers.py
from dropshipping.utils.exchanges import convert_currency

def prepare_product_with_conversion(product, session):
    selected_currency = session.get("currency", "COP")
    converted_price = convert_currency(product.end_price, "COP", selected_currency)
    converted_offer_price = convert_currency(product.offer_price, "COP", selected_currency)
    product.converted_price = round(converted_price, 2)
    product.converted_offer_price = round(converted_offer_price, 2)
    product.currency = selected_currency
    return product
