from django.shortcuts import render ,get_object_or_404
from .models import Product

def product_list(request):
    category = request.GET.get('category')  # Get category from URL params
    if category:
        products = Product.objects.filter(category=category)  # Filter products
    else:
        products = Product.objects.all()  # Show all products

    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})