from django.contrib import messages
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from cart.models import Cart_items

def payment_page(request):
    cart_items = Cart_items.objects.filter(cart__user=request.user)
    if not cart_items.exists():
        messages.error(request, 'Please make sure your cart contain atleast one item')
        return redirect('show_products')
    total = sum(item.total_price() for item in cart_items)


    return render(request, 'payments/payment.html', {'total': total})