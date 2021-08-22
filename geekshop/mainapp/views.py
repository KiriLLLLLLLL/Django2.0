import random

from django.http import request
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, CategoryMenu
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]

def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products

def products(request, pk=None):

    title = 'каталог'

    category_menu = CategoryMenu.objects.all()

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    if pk is not None:
        if pk <= 1:
            products =Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(CategoryMenu, pk=pk)
            products = Product.objects.filter(category_menu__pk=pk).order_by('price')

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)


        context = {
            'title': title,
            'category_menu': category_menu,
            'category': category,
            'products': products_paginator,
            'related_products': same_products,
            'hot_product': hot_product,


        }
        return render(request, 'mainapp/products.html', context)

    products = Product.objects.all().order_by('price')

    context = {
        'title': title,
        'related_products': same_products,
        'category_menu': category_menu,
        'products': products,

        'hot_product': hot_product,
    }

    return render(request, 'mainapp/products.html', context)


def product(request, pk):
    title = 'продукт'


    category_menu = CategoryMenu.objects.all()

    product = get_object_or_404(Product, pk=pk)
    same_products = get_same_products(product)

    context = {
        'title': title,
        'category_menu': category_menu,
        'related_products': same_products,

        'product':product,

    }
    return render(request, 'mainapp/product.html', context)