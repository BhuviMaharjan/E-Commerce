from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem
from django.contrib import messages
from django.views.decorators.http import require_POST

# Create your views here.

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.info(request, 'Increased quantity in cart.')
    else:
        messages.success(request, 'Added to cart!')
    return redirect('cart_page')

@login_required
def cart_page(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'orders/cart.html', {'cart': cart, 'items': items, 'total': total})

@login_required
@require_POST
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated.')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
    except ValueError:
        messages.error(request, 'Invalid quantity.')
    return redirect('cart_page')

@login_required
@require_POST
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart_page')

@login_required
def order_history(request):
    orders = request.user.orders.prefetch_related('items__product').order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()
    total = sum(item.product.price * item.quantity for item in items)
    if request.method == 'POST':
        if not items:
            messages.error(request, 'Your cart is empty.')
            return redirect('cart_page')
        payment_method = request.POST.get('payment_method')
        shipping_address = request.POST.get('shipping_address')
        if not shipping_address:
            messages.error(request, 'Shipping address is required.')
            return redirect('checkout')
        if payment_method != 'cash':
            messages.error(request, 'Invalid payment method.')
            return redirect('checkout')
        # Create order
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            status='pending',
        )
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
        # Clear cart
        cart.items.all().delete()
        messages.success(request, 'Order placed successfully!')
        return redirect('order_history')
    return render(request, 'orders/checkout.html', {'cart': cart, 'items': items, 'total': total, 'user': request.user})

@login_required
@require_POST
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, f'Order #{order.id} cancelled.')
    else:
        messages.error(request, 'Only pending orders can be cancelled.')
    return redirect('order_history')
