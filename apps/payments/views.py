from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from apps.orders.models import Order
from .models import Payment
from .services import NowPaymentsService
import json

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        service = NowPaymentsService()
        success_url = request.build_absolute_uri(reverse('payments:success'))
        cancel_url = request.build_absolute_uri(reverse('payments:failed'))
        ipn_callback_url = request.build_absolute_uri(reverse('payments:webhook'))
        
        invoice = service.create_invoice(
            order_id=order.id,
            price_amount=order.get_total_cost(),
            price_currency='usd', # Assuming USD for now, or get from settings
            ipn_callback_url=ipn_callback_url,
            success_url=success_url,
            cancel_url=cancel_url
        )
        
        if invoice:
            Payment.objects.create(
                order=order,
                transaction_id=invoice.get('id'),
                amount=order.get_total_cost(),
                currency='usd',
                status='pending'
            )
            return redirect(invoice.get('invoice_url'))
        else:
            return redirect('payments:failed')
            
    return render(request, 'payments/process.html', {'order': order})

def payment_success(request):
    if 'order_id' in request.session:
        del request.session['order_id']
    return render(request, 'payments/success.html')

def payment_failed(request):
    return render(request, 'payments/failed.html')

@csrf_exempt
def payment_webhook(request):
    if request.method == 'POST':
        service = NowPaymentsService()
        sig = request.headers.get('x-nowpayments-sig')
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON')

        if service.verify_signature(data, sig):
            payment_status = data.get('payment_status')
            order_id = data.get('order_id')
            
            try:
                order = Order.objects.get(id=order_id)
                payment = Payment.objects.get(order=order)
                
                payment.status = payment_status
                payment.save()
                
                if payment_status == 'finished' or payment_status == 'confirmed':
                    order.paid = True
                    order.status = 'processing' # Or whatever status logic
                    order.save()
                    
                    # Launch asynchronous task
                    from apps.orders.tasks import send_payment_success_email
                    send_payment_success_email.delay(order.id)
                    
            except Order.DoesNotExist:
                pass # Log error
            except Payment.DoesNotExist:
                pass # Log error
                
            return HttpResponse('OK')
        else:
            return HttpResponseBadRequest('Invalid Signature')
    return HttpResponseBadRequest('Invalid Method')
