from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Wishlist

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def wishlist_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    next_url = request.META.get('HTTP_REFERER') or 'wishlist'
    return redirect(next_url)

@login_required
def wishlist_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    next_url = request.META.get('HTTP_REFERER') or 'wishlist'
    return redirect(next_url)