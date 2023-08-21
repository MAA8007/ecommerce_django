from django.contrib import admin
from .models import Product, Order,OrderItem,Category


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'total_price')

class OrderItemInline(admin.TabularInline): # or use admin.StackedInline for a different display style
    model = OrderItem
    extra = 1  # Number of empty forms to display

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ordered_at', 'first_name', 'last_name', 'address', 'zip_code', 'city', 'country', 'phone', 'email', 'payment_method')
    inlines = [OrderItemInline]  # This will show OrderItems inline within the Order

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Product)
admin.site.register(Category)



from .models import Size

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['size', 'size_type']



