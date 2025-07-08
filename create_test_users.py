from users.models import User
from products.models import Product, Category
from orders.models import Order, OrderItem
from django.utils import timezone
import random

# Admin user
if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_user(
        username='admin',
        email='admin@example.com',
        phone_number='9999999999',
        address='Admin Address',
        password='adminpass123',
        role='admin',
        is_approved=True,
    )
    print('Admin user created.')
else:
    print('Admin user already exists.')

# Buyer user
if not User.objects.filter(email='buyer@example.com').exists():
    User.objects.create_user(
        username='testbuyer',
        email='buyer@example.com',
        phone_number='8888888888',
        address='Buyer Address',
        password='buyerpass123',
        role='buyer',
        is_approved=True,
    )
    print('Buyer user created.')
else:
    print('Buyer user already exists.')

# Seller user
if not User.objects.filter(email='seller@example.com').exists():
    User.objects.create_user(
        username='testseller',
        email='seller@example.com',
        phone_number='7777777777',
        address='Seller Address',
        password='sellerpass123',
        role='seller',
        is_approved=True,  # Approve seller
    )
    print('Seller user created.')
else:
    print('Seller user already exists.')

# Create a new seller and buyer for bulk test data
if not User.objects.filter(email='bulkseller@example.com').exists():
    bulkseller = User.objects.create_user(
        username='bulkseller',
        email='bulkseller@example.com',
        phone_number='6666666666',
        address='Bulk Seller Address',
        password='bulksellerpass',
        role='seller',
        is_approved=True,
    )
    print('Bulk seller created.')
else:
    bulkseller = User.objects.get(email='bulkseller@example.com')
    print('Bulk seller already exists.')

if not User.objects.filter(email='bulkbuyer@example.com').exists():
    bulkbuyer = User.objects.create_user(
        username='bulkbuyer',
        email='bulkbuyer@example.com',
        phone_number='5555555555',
        address='Bulk Buyer Address',
        password='bulkbuyerpass',
        role='buyer',
        is_approved=True,
    )
    print('Bulk buyer created.')
else:
    bulkbuyer = User.objects.get(email='bulkbuyer@example.com')
    print('Bulk buyer already exists.')

# Ensure at least one category exists
category, _ = Category.objects.get_or_create(name='General')

# Create 10 products for the new seller
product_objs = []
for i in range(1, 11):
    product, created = Product.objects.get_or_create(
        name=f'Bulk Product {i}',
        defaults={
            'description': f'Description for Bulk Product {i}',
            'price': random.randint(100, 1000),
            'image': 'product_images/Untitled.png',  # Use a placeholder image
            'category': category,
            'seller': bulkseller,
        }
    )
    product_objs.append(product)
    if created:
        print(f'Product {product.name} created.')
    else:
        print(f'Product {product.name} already exists.')

# Create 10 orders for the new buyer, each with 1-3 random products
for i in range(1, 11):
    order = Order.objects.create(
        user=bulkbuyer,
        shipping_address=bulkbuyer.address,
        status=random.choice(['pending', 'shipped', 'delivered']),
        created_at=timezone.now()
    )
    num_items = random.randint(1, 3)
    products_in_order = random.sample(product_objs, num_items)
    for product in products_in_order:
        quantity = random.randint(1, 5)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )
    print(f'Order {order.id} created with {num_items} items.') 