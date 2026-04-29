from django.shortcuts import render

# Create your views here.

from products.models import Category

def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})