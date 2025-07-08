from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Tag
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProductForm, CategoryForm, TagForm
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import ProtectedError
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST

# Create your views here.

def store(request):
    categories = Category.objects.all()
    category_products = []
    for category in categories:
        top_products = category.products.all().order_by('-created_at')[:4]  # Top 4 from each category
        category_products.append((category, top_products))
    return render(request, 'products/store.html', {'category_products': category_products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_by_category = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]
    related_by_tags = Product.objects.filter(tags__in=product.tags.all()).exclude(pk=product.pk).distinct()[:4]
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_by_category': related_by_category,
        'related_by_tags': related_by_tags,
    })

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            messages.error(request, 'You must be an admin to access this page.')
            return redirect('landing')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def seller_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'seller' or not request.user.is_approved:
            messages.error(request, 'You must be an approved seller to access this page.')
            return redirect('profile_dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
@admin_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        form.fields['category'].queryset = Category.objects.all()
        form.fields['tags'].queryset = Tag.objects.all()
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            form.save_m2m()
            messages.success(request, 'Product added successfully!')
            return redirect('manage_products')
    else:
        form = ProductForm()
        form.fields['category'].queryset = Category.objects.all()
        form.fields['tags'].queryset = Tag.objects.all()
    return render(request, 'products/add_product.html', {'form': form})

@login_required
@admin_required
def manage_products(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'products/manage_products.html', {'products': products})

@login_required
@admin_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added!')
            return redirect('add_product')
    else:
        form = CategoryForm()
    return render(request, 'products/add_category.html', {'form': form})

@login_required
@admin_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag added!')
            return redirect('add_product')
    else:
        form = TagForm()
    return render(request, 'products/add_tag.html', {'form': form})

@login_required
@admin_required
def manage_categories(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'products/manage_categories.html', {'categories': categories})

@login_required
@admin_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated!')
            return redirect('manage_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'products/edit_category.html', {'form': form, 'category': category})

@login_required
@admin_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        try:
            category.delete()
            messages.success(request, 'Category deleted!')
            return redirect('manage_categories')
        except ProtectedError:
            messages.error(request, 'Cannot delete: Category is in use by products.')
            return redirect('manage_categories')
    return render(request, 'products/delete_category.html', {'category': category})

@login_required
@admin_required
def manage_tags(request):
    tags = Tag.objects.all().order_by('name')
    return render(request, 'products/manage_tags.html', {'tags': tags})

@login_required
@admin_required
def edit_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag updated!')
            return redirect('manage_tags')
    else:
        form = TagForm(instance=tag)
    return render(request, 'products/edit_tag.html', {'form': form, 'tag': tag})

@login_required
@admin_required
def delete_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        if tag.products.exists():
            messages.error(request, 'Cannot delete: Tag is in use by products.')
            return redirect('manage_tags')
        tag.delete()
        messages.success(request, 'Tag deleted!')
        return redirect('manage_tags')
    return render(request, 'products/delete_tag.html', {'tag': tag})

@login_required
@seller_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        form.fields['category'].queryset = Category.objects.all()
        form.fields['tags'].queryset = Tag.objects.all()
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            form.save_m2m()
            messages.success(request, 'Product added successfully!')
            return redirect('manage_products')
    else:
        form = ProductForm()
        form.fields['category'].queryset = Category.objects.all()
        form.fields['tags'].queryset = Tag.objects.all()
    return render(request, 'products/add_product.html', {'form': form})

@login_required
@seller_required
def manage_products(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'products/manage_products.html', {'products': products})

@login_required
@seller_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        form.fields['category'].queryset = Category.objects.all()
        form.fields['tags'].queryset = Tag.objects.all()
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('manage_products')
    else:
        form = ProductForm(instance=product)
        form.fields['category'].queryset = Category.objects.all()
        form.fields['tags'].queryset = Tag.objects.all()
    return render(request, 'products/add_product.html', {'form': form, 'edit_mode': True, 'product': product})

@login_required
@seller_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('manage_products')
    return render(request, 'products/delete_product.html', {'product': product})

@login_required
def seller_orders(request):
    if request.user.role != 'seller':
        return redirect('landing')
    # Get all orders that include products sold by this seller
    from orders.models import Order, OrderItem
    order_items = OrderItem.objects.filter(product__seller=request.user).select_related('order', 'product')
    order_ids = order_items.values_list('order_id', flat=True).distinct()
    orders = Order.objects.filter(id__in=order_ids).order_by('-created_at').prefetch_related('items__product')
    return render(request, 'orders/seller_orders.html', {'orders': orders, 'order_items': order_items})

@login_required
@require_POST
def mark_order_delivered(request, order_id):
    from orders.models import Order, OrderItem
    order = get_object_or_404(Order, id=order_id)
    # Only allow if the current seller has a product in this order
    if not OrderItem.objects.filter(order=order, product__seller=request.user).exists():
        return redirect('seller_orders')
    order.status = 'delivered'
    order.save()
    messages.success(request, f'Order #{order.id} marked as completed.')
    return redirect('seller_orders')
