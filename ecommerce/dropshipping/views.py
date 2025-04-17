# dropshipping/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models.productModel import Products  
from .forms.form_checkout import CustomerInfoForm, DeliveryInfoForm, PaymentInfoForm

def index(request):
    products = Products.objects.prefetch_related('images').all()
    context = {
        "title": "shingy",
        "product_rating": 3.2,
        "products": products,
        "rating_range": range(1, 6),
    }
    return render(request, 'index.html', context)

def detailProduct(request, product_id):
    product = get_object_or_404(Products.objects.prefetch_related('images').all(), product_id=product_id)
    
    
    context = {
        "title": "shingy",
        "product_rating": 3.2,
        "product": product,
        "rating_range": range(1, 6), 
    }
    return render(request, 'products/detail.html', context)

def checkout(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Products, product_id=product_id)
        
        # Aquí procesarías el pago
        # Redirigir a pasarela de pago o procesar directamente
        
        return render(request, 'checkout/process.html', {
            'product': product,
            'title': 'Proceso de pago'
        })
    
    return redirect('product_detail', product_id=product_id)

def checkout_step1(request, product_id):
    product = get_object_or_404(Products, product_id=product_id)
    
    if request.method == 'POST':
        form = CustomerInfoForm(request.POST)
        if form.is_valid():
            request.session['customer_info'] = form.cleaned_data
            return redirect('checkout_step2', product_id=product_id)
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