"""
Utility functions for tracking and getting recommendations
"""
from .models import ProductView
from .engine import RecommendationEngine


def track_product_view(request, product):
    """
    Track that a user/session viewed a product.
    Call this from product_detail view.
    """
    if request.user.is_authenticated:
        # Logged-in user
        view, created = ProductView.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'view_count': 1}
        )
        if not created:
            view.view_count += 1
            view.save()
    elif request.session.session_key:
        # Guest user with session
        view, created = ProductView.objects.get_or_create(
            session_key=request.session.session_key,
            product=product,
            user=None,
            defaults={'view_count': 1}
        )
        if not created:
            view.view_count += 1
            view.save()


def get_recommendations(request, product=None, limit=6):
    """
    Get personalized recommendations.
    
    Args:
        request: HTTP request object
        product: If provided, get "You may also like" for this product
        limit: Maximum number of recommendations
    
    Returns:
        List of Product objects
    """
    engine = RecommendationEngine(request)
    
    if product:
        return engine.get_recommendations_for_product(product, limit=limit)
    else:
        return engine.get_personalized_recommendations(limit=limit)


def get_homepage_recommendations(request, limit=8):
    """
    Get recommendations for homepage "Recommended for You" section.
    """
    engine = RecommendationEngine(request)
    return engine.get_personalized_recommendations(limit=limit)
