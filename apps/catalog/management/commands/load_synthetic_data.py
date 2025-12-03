from django.core.management.base import BaseCommand
from apps.catalog.models import Category, Product
from decimal import Decimal

class Command(BaseCommand):
    help = 'Loads synthetic data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading synthetic data...')

        # Create Categories
        glasses_cat, _ = Category.objects.get_or_create(
            name='Glasses',
            defaults={'description': 'Optical frames for everyday use.'}
        )
        sunglasses_cat, _ = Category.objects.get_or_create(
            name='Sunglasses',
            defaults={'description': 'Stylish protection from the sun.'}
        )

        self.stdout.write(f'Created categories: {glasses_cat}, {sunglasses_cat}')

        # Product Data from Screenshot
        products_data = [
            {
                'name': 'Heavenly 02',
                'price': 295.00,
                'description': 'Minimalist silver metal frame with a sleek design.',
                'material': 'Metal',
                'shape': 'Rectangular',
                'color': 'Silver',
                'brand': 'Gentle Monster',
                'collection': '2025 Collection',
                'lens_type': 'Clear Blue Light Filter',
                'lens_features': 'Blue Light Protection, UV Protection',
                'manufacturer': 'IICOMBINED CO., LTD.',
                'country_of_origin': 'China',
                'lens_width_mm': 52.0,
                'bridge_width_mm': 21.0,
                'frame_width_mm': 145.0,
                'temple_length_mm': 148.0,
                'lens_height_mm': 35.0,
            },
            {
                'name': 'Rollie 02',
                'price': 270.00,
                'description': 'Elegant oval frames with a modern twist.',
                'material': 'Titanium',
                'shape': 'Oval',
                'color': 'Silver',
                'brand': 'Gentle Monster',
                'collection': '2025 Collection',
                'lens_type': 'Clear Demo Lenses',
                'lens_features': 'UV Protection',
                'manufacturer': 'IICOMBINED CO., LTD.',
                'country_of_origin': 'China',
                'lens_width_mm': 51.5,
                'bridge_width_mm': 20.0,
                'frame_width_mm': 142.0,
                'temple_length_mm': 150.0,
                'lens_height_mm': 33.0,
            },
            {
                'name': 'Lolos 02',
                'price': 260.00,
                'description': 'Classic round metal frames for a sophisticated look.',
                'material': 'Stainless Steel',
                'shape': 'Round',
                'color': 'Silver',
                'brand': 'Gentle Monster',
                'collection': '2025 Collection',
                'lens_type': 'Clear',
                'lens_features': 'Anti-reflective coating',
                'manufacturer': 'IICOMBINED CO., LTD.',
                'country_of_origin': 'Korea',
                'lens_width_mm': 50.0,
                'bridge_width_mm': 22.0,
                'frame_width_mm': 140.0,
                'temple_length_mm': 145.0,
                'lens_height_mm': 45.0,
            },
            {
                'name': 'Boba 02',
                'price': 295.00,
                'description': 'Bold and stylish frames that make a statement.',
                'material': 'Acetate & Metal',
                'shape': 'Cat-eye',
                'color': 'Silver',
                'brand': 'Gentle Monster',
                'collection': 'Bold Collection',
                'lens_type': 'Clear',
                'lens_features': 'Blue Light Filter',
                'manufacturer': 'IICOMBINED CO., LTD.',
                'country_of_origin': 'China',
                'lens_width_mm': 53.0,
                'bridge_width_mm': 19.0,
                'frame_width_mm': 146.0,
                'temple_length_mm': 152.0,
                'lens_height_mm': 38.0,
            },
            {
                'name': 'Limes 02',
                'price': 280.00,
                'description': 'Sharp and edgy design for the fashion-forward.',
                'material': 'Metal',
                'shape': 'Geometric',
                'color': 'Silver',
                'brand': 'Gentle Monster',
                'collection': '2025 Collection',
                'lens_type': 'Clear',
                'lens_features': 'UV Protection',
                'manufacturer': 'IICOMBINED CO., LTD.',
                'country_of_origin': 'China',
                'lens_width_mm': 54.0,
                'bridge_width_mm': 18.0,
                'frame_width_mm': 144.0,
                'temple_length_mm': 147.0,
                'lens_height_mm': 36.0,
            },
            {
                'name': 'Moody 02',
                'price': 270.00,
                'description': 'Versatile frames that suit any mood or occasion.',
                'material': 'Titanium',
                'shape': 'Square',
                'color': 'Silver',
                'brand': 'Gentle Monster',
                'collection': 'Everyday Collection',
                'lens_type': 'Clear',
                'lens_features': 'Blue Light Protection',
                'manufacturer': 'IICOMBINED CO., LTD.',
                'country_of_origin': 'Korea',
                'lens_width_mm': 52.5,
                'bridge_width_mm': 20.5,
                'frame_width_mm': 143.0,
                'temple_length_mm': 149.0,
                'lens_height_mm': 39.0,
            },
        ]

        for p_data in products_data:
            product, created = Product.objects.get_or_create(
                name=p_data['name'],
                defaults={
                    'category': glasses_cat,
                    'price': Decimal(str(p_data['price'])),
                    'description': p_data['description'],
                    'material': p_data['material'],
                    'shape': p_data['shape'],
                    'color': p_data['color'],
                    'brand': p_data['brand'],
                    'collection': p_data['collection'],
                    'lens_type': p_data['lens_type'],
                    'lens_features': p_data['lens_features'],
                    'manufacturer': p_data['manufacturer'],
                    'country_of_origin': p_data['country_of_origin'],
                    'lens_width_mm': Decimal(str(p_data['lens_width_mm'])),
                    'bridge_width_mm': Decimal(str(p_data['bridge_width_mm'])),
                    'frame_width_mm': Decimal(str(p_data['frame_width_mm'])),
                    'temple_length_mm': Decimal(str(p_data['temple_length_mm'])),
                    'lens_height_mm': Decimal(str(p_data['lens_height_mm'])),
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exists: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded synthetic data.'))
