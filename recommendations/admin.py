from django.contrib import admin
from .models import ProductView


@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'session_key', 'view_count', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['product__name', 'user__username']
    ordering = ['-viewed_at']
