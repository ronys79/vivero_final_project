from .models import Category

def category_dropdown(request):
    return {
       'categories': Category.objects.all(),
    }