from django.shortcuts import render
from store.models import Product, ReviewRating

def home(request):
# filter out the not available products, can adjust to out of stock as well
    products = Product.objects.all().filter(is_available=True).order_by('-created_date')
    products = sorted(products, key=lambda prod:prod.averageReview, reverse=True)

    for product in products:
    # Get the reviews
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': products,
        'reviews': reviews,
    }

    return render(request, 'home.html', context)