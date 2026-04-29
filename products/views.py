from django.contrib import redirects
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product

def show_products(request):
    products=Product.objects.filter(available=True)
    return render(request,'products/product_list.html',{'products':products})

from .forms import ReviewForm
from .models import Review
from django.db.models import Avg

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    reviews = product.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                return redirect('product_detail', slug=slug)
    else:
        form = ReviewForm()

    return render(request, 'products/product_details.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
        'average_rating': average_rating
    })

from django.db.models import Q

def search_products(request):
    query = request.GET.get('q')

    products = []

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'products/search_result.html', {
        'products': products,
        'query': query
    })

from .models import Category

def products_by_category(request, slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category)
    sort=request.GET.get('sort')
    if sort=='price_low':
        products=products.order_by('price')
    elif sort=='price_high':
        products.product.order_by('-price')

    elif sort=='name':
        products=products.order_by('name')



    return render(request, 'products/product_list.html', {
        'products': products, 'sort':sort , 'selected_category':category
        # 'selected_category': category
    })

def product_list(request):
    products=Product.objects.all()
    sort=request.GET.get('sort')

    if sort=='price_low':
        products = products.order_by('price')

    elif sort=='price_high':
        products=products.order_by('-price')

    elif sort=='name':
        products=products.order_by('name')

    return render(request, 'products/product_list.html' , {'products':products , 'sort':sort})


# def products_by_category(request, slug):
#     category = Category.objects.get(slug=slug)
#     products = Product.objects.filter(category=category)
#
#     return render(request, 'products/product_list.html', {
#         'products': products
#     })

