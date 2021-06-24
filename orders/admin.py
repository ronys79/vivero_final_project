from django.contrib import admin
from .models import Payment, Order, OrderProduct

# append a table of data
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extract = 0
    #  to make fields non-editable on panel
    readonly_fields = ['payment', 'user', 'order', 'product_price', 'quantity', 'product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'full_name', 'phone', 'email']
    list_per_page = 25
    # append a table of data
    inlines = [OrderProductInline]

admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)

