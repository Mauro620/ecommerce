# dropshipping/forms.py
from django import forms
from django.core.validators import RegexValidator


class CustomerInfoForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre',
            'required': 'required'
        }),
        max_length=100,
        label=''
    )
    
    surname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellido',
            'required': 'required'
        }),
        max_length=100,
        label=''
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico',
            'required': 'required'
        }),
        label=''
    )
    
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Numero de Celular',
            'required': 'required'
        }),
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="El número de teléfono debe tener entre 9 y 15 dígitos."
            )
        ],
        label=''
    )
    
    newsletter = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input ml-2 mt-3',
        }),
        label='Recibir ofertas y promociones:'
    )

class DeliveryInfoForm(forms.Form):
    country = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            # 'placeholder': 'País',
            'required': 'required'
        }),
        label='País'
    )
    # country = forms.CharField(label='País', max_length=100)
    state = forms.CharField(
        label='Estado/Departamento',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            # 'placeholder': 'Estado/Departamento',
            'required': 'required'
        })
        )
    city = forms.CharField(label='Ciudad', max_length=100)
    address = forms.CharField(label='Dirección', widget=forms.TextInput(attrs={}))
    postal_code = forms.CharField(label='Código Postal', max_length=20)
    additional_info = forms.CharField(
        label='Información Adicional', 
        required=False,
        widget=forms.TextInput(attrs={})
    )

class PaymentInfoForm(forms.Form):
    CARD_TYPES = (
        ('visa', 'Visa'),
        ('mastercard', 'MasterCard'),
        ('amex', 'American Express'),
    )
    
    card_type = forms.ChoiceField(
        label='Tipo de Tarjeta', 
        choices=CARD_TYPES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    card_number = forms.CharField(label='Número de Tarjeta', max_length=19)
    card_name = forms.CharField(label='Nombre en la Tarjeta', max_length=100)
    expiry_date = forms.CharField(label='Fecha de Expiración (MM/AA)', max_length=5)
    cvv = forms.CharField(label='CVV', max_length=4, widget=forms.PasswordInput())