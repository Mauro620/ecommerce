from django.shortcuts import render, redirect, get_object_or_404
from dropshipping.models.productModel import Products
from dropshipping.forms.formCheckout import CustomerInfoForm, DeliveryInfoForm, PaymentInfoForm
from django.contrib import messages
from dropshipping.utils.exchanges import convert_currency

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
    product = get_object_or_404(Products, product_id=product_id)

    selected_currency = request.session.get("currency", "COP")

    converted_price = convert_currency(product.end_price, "COP", selected_currency)
    converted_offer_price = convert_currency(product.offer_price, "COP", selected_currency)
    product.converted_price = round(converted_price, 2)
    product.converted_offer_price = round(converted_offer_price, 2)
    product.currency = selected_currency
    
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
    product = get_object_or_404(Products, product_id=product_id)
    
    if 'customer_info' not in request.session:
        return redirect('checkout_step1', product_id=product_id)
    
    if request.method == 'POST':
        form = DeliveryInfoForm(request.POST)
        if form.is_valid():
            request.session['delivery_info'] = form.cleaned_data
            return redirect('checkout_step3', product_id=product_id)
    else:
        form = DeliveryInfoForm()
    
    context = {
        'product': product,
        'form': form,
        'current_step': 2,
        'total_steps': 3,
    }
    return render(request, 'checkout/step2.html', context)

def checkout_step3(request, product_id):
    product = get_object_or_404(Products, product_id=product_id)
    
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
    # Aquí procesarías el pago realmente
    return render(request, 'checkout/complete.html')