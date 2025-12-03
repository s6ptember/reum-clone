from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from apps.catalog.models import Product
from .cart import Cart
import json

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    
    if request.headers.get('HX-Request'):
        response = render(request, 'cart/partials/cart_drawer.html', {'cart': cart})
        response['HX-Trigger'] = json.dumps({
            'open-cart': True, 
            'update-cart-count': len(cart)
        })
        return response
    
    return redirect('catalog:product_list')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    
    if request.headers.get('HX-Request'):
        response = render(request, 'cart/partials/cart_drawer.html', {'cart': cart})
        response['HX-Trigger'] = json.dumps({
            'update-cart-count': len(cart)
        })
        return response
    
    return redirect('catalog:product_list')

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity, override_quantity=True)
    
    if request.headers.get('HX-Request'):
        response = render(request, 'cart/partials/cart_drawer.html', {'cart': cart})
        response['HX-Trigger'] = json.dumps({
            'update-cart-count': len(cart)
        })
        return response
    
    return redirect('catalog:product_list')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/partials/cart_drawer.html', {'cart': cart})
