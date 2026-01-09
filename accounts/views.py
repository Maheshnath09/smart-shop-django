from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from orders.models import Order
from .models import Profile
from .forms import ProfileForm

#view to handle user signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # Create profile on signup
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})
#view to handle user logout
def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html')  # Render logout page instead of redirect

#view to display user profile and their orders

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'orders': orders, 'profile': profile})


@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save(request.user)
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, user=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})