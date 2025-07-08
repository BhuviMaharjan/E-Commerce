from django.shortcuts import render, redirect, get_object_or_404
from users.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.

def landing(request):
    return render(request, 'core/landing.html')

@login_required
def admin_dashboard(request):
    if not request.user.role == 'admin':
        return redirect('landing')
    users = User.objects.exclude(role='admin').order_by('-date_joined')
    return render(request, 'core/admin_dashboard.html', {'users': users})

@login_required
def approve_seller(request, user_id):
    if not request.user.role == 'admin':
        return redirect('landing')
    user = get_object_or_404(User, id=user_id)
    user.is_approved = True
    user.save()
    messages.success(request, f"Seller {user.username} approved.")
    return redirect('admin_dashboard')

@login_required
def block_user(request, user_id):
    if not request.user.role == 'admin':
        return redirect('landing')
    user = get_object_or_404(User, id=user_id)
    user.is_blocked = True
    user.save()
    messages.success(request, f"User {user.username} blocked.")
    return redirect('admin_dashboard')

@login_required
def unblock_user(request, user_id):
    if not request.user.role == 'admin':
        return redirect('landing')
    user = get_object_or_404(User, id=user_id)
    user.is_blocked = False
    user.save()
    messages.success(request, f"User {user.username} unblocked.")
    return redirect('admin_dashboard')

@login_required
def change_user_role(request, user_id):
    if not request.user.role == 'admin':
        return redirect('landing')
    user = get_object_or_404(User, id=user_id)
    buyer_seller_roles = [(v, l) for v, l in User.ROLE_CHOICES if v in ['buyer', 'seller']]
    if request.method == 'POST':
        new_role = request.POST.get('role')
        if new_role in dict(buyer_seller_roles):
            user.role = new_role
            user.save()
            messages.success(request, f"Role for {user.username} changed to {new_role}.")
        return redirect('admin_dashboard')
    return render(request, 'core/change_user_role.html', {'user': request.user, 'target_user': user, 'roles': buyer_seller_roles})

@login_required
def add_user(request):
    if not request.user.role == 'admin':
        return redirect('landing')
    buyer_seller_roles = [(v, l) for v, l in User.ROLE_CHOICES if v in ['buyer', 'seller']]
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        role = request.POST.get('role')
        password = request.POST.get('password')
        if email and username and password:
            user = User.objects.create_user(username=username, email=email, phone_number=phone_number, address=address, password=password, role=role)
            messages.success(request, f"User {username} added.")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "All fields are required.")
    return render(request, 'core/add_user.html', {'roles': buyer_seller_roles})

@login_required
def edit_user(request, user_id):
    if not request.user.role == 'admin':
        return redirect('landing')
    user = get_object_or_404(User, id=user_id)
    buyer_seller_roles = [(v, l) for v, l in User.ROLE_CHOICES if v in ['buyer', 'seller']]
    if request.method == 'POST':
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        user.phone_number = request.POST.get('phone_number')
        user.address = request.POST.get('address')
        user.role = request.POST.get('role')
        user.save()
        messages.success(request, f"User {user.username} updated.")
        return redirect('admin_dashboard')
    return render(request, 'core/edit_user.html', {'user': request.user, 'target_user': user, 'roles': buyer_seller_roles})

@login_required
def delete_user(request, user_id):
    if not request.user.role == 'admin':
        return redirect('landing')
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted.")
        return redirect('admin_dashboard')
    return render(request, 'core/delete_user.html', {'user': user})

@login_required
def admin_profile_dashboard(request):
    user = request.user
    if user.role != 'admin':
        return redirect('profile_dashboard')
    return render(request, 'users/admin_profile_dashboard.html', {'user': user})
