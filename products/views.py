from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.db.models import Q  # For search
from wishlist.models import Wishlist
from recommendations.utils import track_product_view, get_recommendations, get_homepage_recommendations

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    wishlist_product_ids = []
    if request.user.is_authenticated:
        wishlist_product_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
    
    # Get personalized recommendations
    recommendations = get_homepage_recommendations(request, limit=8)
    
    return render(request, 'products/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'wishlist_product_ids': wishlist_product_ids,
        'recommendations': recommendations,
    })

def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug, available=True)
    cart_product_form = CartAddProductForm()
    is_in_wishlist = False
    if request.user.is_authenticated:
        is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    
    # Track this product view for recommendations
    track_product_view(request, product)
    
    # Get "You may also like" recommendations
    similar_products = get_recommendations(request, product=product, limit=6)
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'is_in_wishlist': is_in_wishlist,
        'similar_products': similar_products,
    })

def product_search(request):
    query = request.GET.get('query')
    categories = Category.objects.all()
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query), available=True
        )
    else:
        products = Product.objects.filter(available=True)
    wishlist_product_ids = []
    if request.user.is_authenticated:
        wishlist_product_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
    return render(request, 'products/product_list.html', {
        'category': None,
        'categories': categories,
        'products': products,
        'search_query': query,
        'wishlist_product_ids': wishlist_product_ids,
    })