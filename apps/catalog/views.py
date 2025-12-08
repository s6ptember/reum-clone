from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, Category

class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'catalog/product_list.html'

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['catalog/partials/product_list_content.html']
        return [self.template_name]

    def get_queryset(self):
        from django.db.models import Q
        queryset = super().get_queryset()
        
        # Search
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(brand__icontains=query)
            )

        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Dimensions filters
        for field in ['lens_width_mm', 'bridge_width_mm', 'frame_width_mm', 'temple_length_mm']:
            value = self.request.GET.get(field)
            if value:
                queryset = queryset.filter(**{field: value})

        # Characteristics filters
        for field in ['shape', 'color', 'material']:
            value = self.request.GET.get(field)
            if value:
                queryset = queryset.filter(**{f'{field}__icontains': value})

        return queryset.select_related('category').prefetch_related('images')

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'catalog/product_detail.html'
    slug_url_kwarg = 'slug'

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['catalog/partials/product_detail_content.html']
        return [self.template_name]

    def get_queryset(self):
        return super().get_queryset().select_related('category').prefetch_related('images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        related_products = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id).prefetch_related('images').order_by('?')[:2]
        context['related_products'] = related_products
        return context
