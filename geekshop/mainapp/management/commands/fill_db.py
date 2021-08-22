from django.core.management.base import BaseCommand
import json
import os

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product, CategoryMenu

JSON_PATH = 'mainapp/jsons'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), encoding='utf-8', mode='r') as infile:
        return json.load(infile)

class Command(BaseCommand):
    def handle(self, *args, **options):

        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()

        menues = load_from_json('menues')

        CategoryMenu.objects.all().delete()
        for menu in menues:
            new_link = CategoryMenu(**menu)
            new_link.save()

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            category_name = product['category']
            cat_menu_name = product['category_menu']

            _category = ProductCategory.objects.get(name=category_name)
            product['category'] = _category
            _cat_menu = CategoryMenu.objects.get(name=cat_menu_name)
            product['category_menu'] = _cat_menu
            new_product = Product(**product)
            new_product.save()




    ShopUser.objects.create_superuser('django1', 'django@geekshop.local', '123', age=33)

