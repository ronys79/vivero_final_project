from django.contrib import admin
from .models import Product, ReviewRating, ProductGallery, Variation
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ProductAdmin(admin.ModelAdmin):
# populate slug to rule out errors + populated field all lower case with hyphen as space
    prepopulated_fields = {'slug': ('product_name',)}
# what to display on admin panel for ref
    list_display = ('category', 'product_name', 'price', 'images', 'stock', 'is_available', 'modified_date')
# clickable links to get to product specific page or quck view image
    list_display_links = ('category', 'product_name', 'images')
    inlines = [ProductGalleryInline]
    
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_description', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_description')

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)