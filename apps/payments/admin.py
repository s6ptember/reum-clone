from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'transaction_id', 'amount', 'currency', 'status', 'provider', 'created_at']
    list_filter = ['status', 'provider', 'created_at']
    search_fields = ['transaction_id', 'order__id', 'order__email']
    readonly_fields = ['created_at', 'updated_at']
