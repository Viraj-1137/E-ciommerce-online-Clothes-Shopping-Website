from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE

from products.models import Product


# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

class Cart_items(models.Model):
    cart=models.ForeignKey(Cart, on_delete=CASCADE)
    product=models.ForeignKey(Product , on_delete=CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price*self.quantity