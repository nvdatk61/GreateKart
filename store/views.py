from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import Cart, CartItem
from carts.views import _cart_id
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True)
        
    else:
        products = Product.objects.all().filter(is_available=True)

    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    page_product = paginator.get_page(page)
    
    product_count = products.count()
    context = {
        'products': page_product,
        'product_count': product_count
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug=None, product_slug=None):
    try:
        product_detail = Product.objects.get( category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product = product_detail).exists()
    except Exception as e:
        raise e
    out_stock = False
    if product_detail.stock <=0:
        out_stock = True
    context = {
        'product_detail': product_detail,
        'out_stock': out_stock,
        'in_cart' : in_cart
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keywords = request.GET['keyword']
        if keywords:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains = keywords) | Q(product_name__icontains = keywords))

    context = {
        'products': products
    }
    return render(request, 'store/store.html', context)

