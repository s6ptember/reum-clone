from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Characteristics
    material = models.CharField(max_length=100, blank=True)
    shape = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    collection = models.CharField(max_length=100, blank=True, help_text="e.g. 2025 FALL Collection")
    lens_type = models.CharField(max_length=100, blank=True, help_text="e.g. Clear Lenses")
    lens_features = models.TextField(blank=True, help_text="e.g. Lenses Block Blue Light and 99.9% of UV Rays")
    manufacturer = models.CharField(max_length=200, blank=True)
    country_of_origin = models.CharField(max_length=100, blank=True)

    # Dimensions
    lens_width_mm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Lens width (mm)")
    bridge_width_mm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Bridge width (mm)")
    frame_width_mm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Frame front (mm)")
    temple_length_mm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Temple length (mm)")
    lens_height_mm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Lens height (mm)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"
