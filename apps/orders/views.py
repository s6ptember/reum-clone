from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from .models import OrderItem, Order
from .forms import OrderCreateForm
from apps.cart.cart import Cart
from apps.payments.services import NowPaymentsService
from apps.payments.models import Payment

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # set the order in the session
            request.session['order_id'] = order.id
            
            # Launch asynchronous task
            from .tasks import send_order_created_email
            send_order_created_email.delay(order.id)
            
            # Create invoice with NowPayments
            service = NowPaymentsService()
            success_url = request.build_absolute_uri(reverse('payments:success'))
            cancel_url = request.build_absolute_uri(reverse('payments:failed'))
            ipn_callback_url = request.build_absolute_uri(reverse('payments:webhook'))
            
            invoice = service.create_invoice(
                order_id=order.id,
                price_amount=order.get_total_cost(),
                price_currency='usd', # TODO: Make dynamic if needed
                ipn_callback_url=ipn_callback_url,
                success_url=success_url,
                cancel_url=cancel_url
            )
            
            if invoice and 'invoice_url' in invoice:
                # Create Payment record
                Payment.objects.create(
                    order=order,
                    transaction_id=invoice.get('id'),
                    amount=order.get_total_cost(),
                    currency='usd',
                    status='pending'
                )
                
                redirect_url = invoice.get('invoice_url')
                if request.headers.get('HX-Request'):
                    response = HttpResponse()
                    response['HX-Redirect'] = redirect_url
                    return response
                return redirect(redirect_url)
            else:
                # Handle error - for now redirect to failed
                if request.headers.get('HX-Request'):
                    response = HttpResponse()
                    response['HX-Redirect'] = reverse('payments:failed')
                    return response
                return redirect('payments:failed')

    else:
        form = OrderCreateForm()
    
    context = {'cart': cart, 'form': form}
    
    if request.headers.get('HX-Request'):
        return render(request, 'orders/order/create_content.html', context)
        
    return render(request, 'orders/order/create.html', context)

def order_detail(request, order_id):
    session_order_id = request.session.get('order_id')
    if str(session_order_id) != str(order_id):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
        
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order/detail.html', {'order': order})
