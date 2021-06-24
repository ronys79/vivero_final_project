from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating, ProductGallery
from carts.models import Cart
from category.models import Category
from carts.models import CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from carts.views import _cart_id
from django.db.models import Q

from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct


def store(request, category_slug=None):
    categories = None
    products = None
    
# what to do if slug is not empty
    if category_slug != None:
        # get page or render 404
        category = get_object_or_404(Category, slug=category_slug)
        # order by function to order in pagination, set to order by id
        products = Product.objects.filter(category=category, is_available=True)
        paginator = Paginator(products, 6)
        #  capturing url page for paginator
        page = request.GET.get('page')
        # storing products captured above to be displayed on html
        paged_products = paginator.get_page(page)
        items_found = products.count()

    else:
        # display all products on store if slug not found so page isnt blank
        products = Product.objects.all().filter(is_available=True).order_by('id')
        # paginator functunality to display qnt of products
        paginator = Paginator(products, 6)
        #  capturing url page for paginator
        page = request.GET.get('page')
        # storing products captured above to be displayed on html
        paged_products = paginator.get_page(page)
        # total products displayed
        items_found = products.count()

    context = {
        'products': paged_products,
        'items_found': items_found,
    }

    return render(request, 'store/store_base.html', context)

def product_detail(request, category_slug, product_slug):
    # to get single view page
    orderproduct = None
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        # check if object added to cart
        # if this query returns any object that may exiest it returns true and if false then object not in cart
        in_cart = Cart.objects.filter(cart_id=_cart_id(request), cartitem__product=single_product).exists()

    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
        else:
            orderproduct = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    # # Get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            # filtering search for now via description
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | 
                Q(product_name__icontains=keyword) | 
                Q(price__icontains=keyword) | 
                Q(category__category_name__icontains=keyword)
                )
            items_found = products.count()

    context = {
        'products': products,
        'items_found': items_found,
        'keyword' : keyword,
    }
    return render(request, 'store/store_base.html', context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)