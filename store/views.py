from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import Cart, CartItems
from carts.views import _cart_id
from django.http import HttpResponse

# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True)
        
    else:
        products = Product.objects.all().filter(is_available=True)
    
    product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug=None, product_slug=None):
    try:
        product_detail = Product.objects.get( category__slug=category_slug, slug=product_slug)
        in_cart = CartItems.objects.filter(cart__cart_id = _cart_id(request), product = product_detail).exists()
        return HttpResponse()
    except Exception as e:
        raise e
    out_stock = False
    if product_detail.stock <=0:
        out_stock = True
    context = {
        'product_detail': product_detail,
        'out_stock': out_stock
    }
    return render(request, 'store/product_detail.html', context)

