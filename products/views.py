from django.shortcuts import render ,get_object_or_404
from .models import Product


CATEGORY_DISPLAY_NAMES = {
    "gym_equipment": "Gym Equipment",
    "clothing": "Clothing",
    "shoes": "Athletic Footwear",
    "supplements": "Supplements",
    "sports_gear": "Sports Gear",
    "all-products": "All Products",
}


def product_list(request, category=None):
    if category and category != "all-products":
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()  # Show all products if "All Products" is selected

    readable_category = CATEGORY_DISPLAY_NAMES.get(category, "All Products")

    return render(request, "products/product_list.html", {"products": products, "selected_category": readable_category})



def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})