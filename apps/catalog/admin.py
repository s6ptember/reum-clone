from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'brand', 'collection', 'created_at')
    list_filter = ('category', 'brand', 'material', 'shape', 'collection')
    search_fields = ('name', 'description', 'brand', 'collection')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    fieldsets = (
        ('General', {
            'fields': ('category', 'name', 'slug', 'description', 'price')
        }),
        ('Characteristics', {
            'fields': ('brand', 'collection', 'material', 'shape', 'color', 'lens_type', 'lens_features', 'manufacturer', 'country_of_origin')
        }),
        ('Dimensions', {
            'fields': ('lens_width_mm', 'bridge_width_mm', 'frame_width_mm', 'temple_length_mm', 'lens_height_mm')
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_main', 'created_at')
