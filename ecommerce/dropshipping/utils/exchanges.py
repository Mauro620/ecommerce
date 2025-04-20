# Simulación de tasas de cambio. En producción usarías una API como fixer.io o exchangerate.host
from decimal import Decimal

exchange_rates = {
    'COP': Decimal('1'),
    'USD': Decimal('0.00025'),
    'EUR': Decimal('0.00023'),
    'MXN': Decimal('0.0043'),
    'ARS': Decimal('0.21'),
    'CLP': Decimal('0.22'),
    'PEN': Decimal('0.0009'),
    'BRL': Decimal('0.0005'),
}

def convert_currency(amount, from_currency, to_currency):
    if from_currency not in exchange_rates or to_currency not in exchange_rates:
        return amount  
    return amount * exchange_rates[to_currency] / exchange_rates[from_currency]
