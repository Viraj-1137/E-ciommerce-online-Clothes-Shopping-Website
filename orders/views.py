from django.shortcuts import redirect, render
from cart.models import Cart_items
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Order, OrderItem
from products.models import Product
from django.contrib.auth.decorators import login_required

@require_POST
@login_required
def checkout(request):
    cart_items = Cart_items.objects.filter(cart__user=request.user)

    if not cart_items.exists():
        messages.error(request, 'cannot place order with empty cart')
        return redirect('show_products')

    total = sum(item.total_price() for item in cart_items)

    order = Order.objects.create(
        user=request.user,
        total_amount=total
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

        # reduce stock
        item.product.stock -= item.quantity
        item.product.save()

    cart_items.delete()
    messages.success(request, "Order placed successfully")
    return redirect('order_success')

def order_success(request):
    return render(request, 'order_success.html')


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})
