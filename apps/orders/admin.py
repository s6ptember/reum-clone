from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'get_transaction_id', 'created_at', 'updated_at']
    list_filter = ['paid', 'created_at', 'updated_at']
    readonly_fields = ['get_transaction_id']
    inlines = [OrderItemInline]

    def get_transaction_id(self, obj):
        if hasattr(obj, 'payment'):
            return obj.payment.transaction_id
        return None
    get_transaction_id.short_description = 'Transaction ID'
