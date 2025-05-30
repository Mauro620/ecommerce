from django.shortcuts import render, redirect, get_object_or_404
from dropshipping.models.productModel import Products
from dropshipping.forms.formCheckout import CustomerInfoForm, DeliveryInfoForm, PaymentInfoForm
from django.contrib import messages
from dropshipping.utils.helpers import prepare_product_with_conversion
from django.http import JsonResponse
from dropshipping.models.addressModel import Country, State, City
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from dropshipping.models import (
    Users, Country, State, City, Address, 
    Orders, OrderDetail, Payments
)
from dropshipping.utils.helpers import prepare_product_with_conversion
import uuid

def checkout(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Products, product_id=product_id)
        
        return render(request, 'checkout/process.html', {
            'product': product,
            'title': 'Proceso de pago'
        })
    
    return redirect('product_detail', product_id=product_id)

def checkout_step1(request, product_id):
    """
    Handles the first step of the checkout process for a specific product.
    This view retrieves the product based on the provided `product_id` and 
    processes the customer's information form. If the form is valid, the 
    customer's data is stored in the session, and the user is redirected 
    to the second step of the checkout process. If the form is invalid, 
    an error message is displayed.
    Args:
        request (HttpRequest): The HTTP request object containing metadata 
            about the request.
        product_id (uuid): The ID of the product being purchased.
    Returns:
        HttpResponse: Renders the checkout step 1 template with the product 
        and form context, or redirects to the next step in the checkout 
        process if the form is successfully submitted.
    Context:
        product (Products): The product object retrieved based on `product_id`.
        form (CustomerInfoForm): The form for collecting customer information.
        current_step (int): The current step in the checkout process (1).
        total_steps (int): The total number of steps in the checkout process (3).
    Template:
        checkout/step1.html
    """
    product = prepare_product_with_conversion(get_object_or_404(Products, product_id=product_id), request.session)

    
    if request.method == 'POST':
        form = CustomerInfoForm(request.POST)
        if form.is_valid():
            request.session['customer_info'] = form.cleaned_data
            return redirect('checkout_step2', product_id=product_id)
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = CustomerInfoForm()
    
    context = {
        'product': product,
        'form': form,
        'current_step': 1,
        'total_steps': 3,
    }
    return render(request, 'checkout/step1.html', context)

def checkout_step2(request, product_id):
    product = prepare_product_with_conversion(get_object_or_404(Products, product_id=product_id), request.session)
    
    if 'customer_info' not in request.session:
        return redirect('checkout_step1', product_id=product_id)
    
    if request.method == 'POST':
        form = DeliveryInfoForm(request.POST)

        country_id = request.POST.get('country')
        state_id = request.POST.get('state')

        if country_id:
            form.fields['state'].queryset = State.objects.filter(country_id=country_id)
        if state_id:
            form.fields['city'].queryset = City.objects.filter(state_id=state_id)
        if form.is_valid():
            delivery_info = {
                'country_id': form.cleaned_data['country'].id,
                'country_name': form.cleaned_data['country'].name,
                'state_id': form.cleaned_data['state'].id,
                'state_name': form.cleaned_data['state'].name,
                'city_id': form.cleaned_data['city'].id,
                'city_name': form.cleaned_data['city'].name,
                'address': form.cleaned_data['address'],
                'postal_code': form.cleaned_data['postal_code'],
                'additional_info': form.cleaned_data['additional_info'],
            }
            request.session['delivery_info'] = delivery_info
            return redirect('checkout_step3', product_id=product_id)

    else:
        form = DeliveryInfoForm()
    
    context = {
        'product': product,
        'form': form,
        'current_step': 2,
        'total_steps': 3,
        'delivery_info': request.session.get('delivery_info', {}),
    }
    return render(request, 'checkout/step2.html', context)

def checkout_step3(request, product_id):
    product = prepare_product_with_conversion(get_object_or_404(Products, product_id=product_id), request.session)

    
    if 'delivery_info' not in request.session:
        return redirect('checkout_step1', product_id=product_id)
    
    if request.method == 'POST':
        form = PaymentInfoForm(request.POST)
        if form.is_valid():
            request.session['payment_info'] = form.cleaned_data
            return redirect('checkout_complete', product_id=product_id)
    else:
        form = PaymentInfoForm()
    
    context = {
        'product': product,
        'form': form,
        'current_step': 3,
        'total_steps': 3,
    }
    return render(request, 'checkout/step3.html', context)

def checkout_complete(request, product_id):
    # Verificar que todos los datos necesarios están en la sesión
    if not all(k in request.session for k in ('customer_info', 'delivery_info', 'payment_info')):
        return redirect('checkout_step1', product_id=product_id)
    
    product = prepare_product_with_conversion(get_object_or_404(Products, product_id=product_id), request.session)
    customer_info = request.session.get('customer_info')
    delivery_info = request.session.get('delivery_info')
    payment_info = request.session.get('payment_info')

    print(customer_info)

    try:
        with transaction.atomic():
            user, create = Users.objects.get_or_create(
                email=customer_info['email'],
                defaults={
                    'name': customer_info['name'],
                    'surname': customer_info['surname'],
                    'phone_number': customer_info['phone_number'],
                }
            )

            country = Country.objects.get(id=delivery_info['country_id'])
            state = State.objects.get(id=delivery_info['state_id'])
            city = City.objects.get(id=delivery_info['city_id'])

            address = Address.objects.create(
                address=delivery_info['address'],
                aditional_info=delivery_info.get('additional_info', ''),
                city=city
            )
            order = Orders.objects.create(
                user=user,
                order_status='pending',
                total_price=product.converted_price
            )

            order_detail = OrderDetail.objects.create(
                product=product,
                order=order,
                quantity=1,
                unit_price=product.converted_price,
                subtotal=product.converted_price,
                address_delivery=address
            )

            payment = Payments.objects.create(
                order=order,
                payment_method=payment_info['card_type'],
                amount=product.converted_price,
                payment_status='completed'
            )

            for key in ('customer_info', 'delivery_info', 'payment_info'):
                request.session.pop(key, None)

    except Exception as e:
        print(f"Error al procesar el pedido: {str(e)}")
        messages.error(request, "Ocurrió un error al procesar tu pedido. Por favor intenta nuevamente.")
        return redirect('checkout_step3', product_id=product_id)

    context = {
        'product': product,
        'customer_info': customer_info,
        'delivery_info': delivery_info,
        'payment_info': payment_info,
        'order': order,
    }

    return render(request, 'checkout/complete.html', context)



def load_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).values('id', 'name')
    return JsonResponse(list(states), safe=False)

def load_cities(request):
    state_id = request.GET.get('state_id')
    cities = City.objects.filter(state_id=state_id).values('id', 'name')
    return JsonResponse(list(cities), safe=False)

