from .models import Cart_items

def cart_item_count(request):
    if request.user.is_authenticated:
        count = Cart_items.objects.filter(cart__user=request.user).count()
    else:
        count = 0

    return {'cart_count': count}