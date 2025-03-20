from django.shortcuts import render, redirect
from django.http import JsonResponse
from cart.models import CartItem
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

# View Cart
@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum([item.total_price for item in cart_items])
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total': total})

# Add Item to Cart
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    quantity = int(request.POST.get('quantity', 1))


    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user, defaults={'quantity': quantity})
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return redirect('cart:view_cart')  # Redirect to the cart page

# Remove Item from Cart
@login_required
def remove_from_cart(request, product_id):
    cart_item = CartItem.objects.get(product_id=product_id, user=request.user)
    cart_item.delete()
    return redirect('cart:view_cart')  # Redirect back to the cart page


def cart_item_count(request):
    if request.user.is_authenticated:
        total_quantity = CartItem.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total']
        return {'cart_item_count': total_quantity if total_quantity else 0}
    return {'cart_item_count': 0}

@login_required
def update_cart(request, product_id):
    cart_item = CartItem.objects.get(product_id=product_id, user=request.user)

    if request.method == "POST":
        action = request.POST.get('action')

        if action == "increase":
            cart_item.quantity += 1
            cart_item.save()
        elif action == "decrease":
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()  # If quantity reaches 0, remove the item

    return redirect('cart:view_cart')  # Redirect back to cart page

def order_confirmation(request):
    order_id = "123456"
    return render(request, 'cart/order-confirmation.html', {'order_id': order_id})


