from collections import Counter
from itertools import count
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from store.forms import Review_form
from .models import Product, Review
from category.models import Category
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.contrib.auth.decorators import login_required

# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products':  paged_products,
        'product_count': product_count, 
        'categories':categories,

    }

    return render(request,'store/store.html', context)


def product_detail(request,id):
    
    
    single_product = Product.objects.get(pk=id)
    reviews = Review.objects.filter(product=single_product)
    # in_cart = CartItem.objects.filter(cart__cart_id)

    
    context = {

        'single_product': single_product,
        'form':Review_form,
        'reviews':reviews
    }    

    return render(request, 'store/product_detail.html',context)

def search(request):
    
       
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()

      
            
    context = {
       'products': products,
       'product_count': product_count,
        
         
     }
    return render(request, 'store/store.html',context)



def filter_price(request):
    if request.method == 'GET':
        min_price = request.GET['min-price']
        max_price = request.GET['max-price']

        if min_price or max_price:
           

            product = Product.objects.filter(price__gte=min_price, price__lte=max_price)
            print(product)
        else:
            product = Product.objects.all()

    context = {
        'products': product,
    }
    return render(request, 'store/store.html', context)


def price_sort(request):
    sort = request.GET.get('sort')
    if sort == 'latest':
        product = Product.objects.all().order_by('publishing_date')
    elif sort == 'price-low':
        product = Product.objects.all().order_by('price')
    elif sort == 'price-high':
        product = Product.objects.all().order_by('-price')
    elif sort == 'name':
        product = Product.objects.all().order_by('title')
    elif sort == 'default':
        product = Product.objects.all().order_by('id')
    else:
        product = Product.objects.all().order_by('id')

    paginator = Paginator(product, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = product.count()
    categories = Category.objects.annotate(
        num_product=Count('product')).values('category_name', 'num_product')


    context = {
        'products':  paged_products,
        'product_count': product_count, 
        'categories':categories,

    }
    return render(request, 'store/store.html',context)



@login_required(login_url='login')
def product_review(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        
        form = Review_form(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', id=id)

        else:
            form = Review_form()
        
    return HttpResponse('success')
    
   