from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart, Cart_items
from products.models import Product


# Create your views here.
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = Cart_items.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, "Item added to cart")
    return redirect('cart_detail')

from django.shortcuts import render

@login_required
def cart_detail(request):
    cart_items = Cart_items.objects.filter(cart__user=request.user)

    total = sum(item.total_price() for item in cart_items)

    return render(request, 'cart/cart_details.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(Cart_items, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart")
    return redirect('cart_detail')

@login_required
def increase_quantity(request, item_id):
    item = Cart_items.objects.get(id=item_id, cart__user=request.user)

    if item.quantity < item.product.stock:
        item.quantity += 1
        item.save()

    return redirect('cart_detail')

@login_required
def decrease_quantity(request, item_id):
    item = Cart_items.objects.get(id=item_id, cart__user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart_detail')