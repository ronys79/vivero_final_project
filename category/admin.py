from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
# auto populate slug field on admin panel to lower chance of  errors when creating categories'
# slug will populate with all lower case characters + hyphen added in spaces
    prepopulated_fields = {'slug': ('category_name',)}

# display collums/field_name on admin panel
    list_display = ('category_name', 'slug', 'cat_image')

admin.site.register(Category, CategoryAdmin)
