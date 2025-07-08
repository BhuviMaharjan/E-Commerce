from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import BuyerRegistrationForm, SellerRegistrationForm, CustomAuthenticationForm, UserEditForm
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.

# Buyer Registration View
def register_buyer(request):
    if request.method == 'POST':
        form = BuyerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = BuyerRegistrationForm()
    return render(request, 'users/register_buyer.html', {'form': form})

# Seller Registration View
def register_seller(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Wait for admin approval before logging in.')
            return redirect('login')
    else:
        form = SellerRegistrationForm()
    return render(request, 'users/register_seller.html', {'form': form})

# Login View
def user_login(request):
    if request.user.is_authenticated:
        return redirect('profile_dashboard')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile_dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# Logout View
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def profile_dashboard(request):
    user = request.user
    if user.role == 'admin':
        return redirect('admin_profile_dashboard')
    return render(request, 'users/profile_dashboard.html', {'user': user})

@login_required
def edit_profile(request):
    user = request.user
    if user.role == 'admin':
        messages.error(request, 'Admin profile cannot be edited here.')
        return redirect('admin_profile_dashboard')
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile_dashboard')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'users/edit_profile.html', {'form': form, 'user': user})
