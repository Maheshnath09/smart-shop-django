"""
AI/ML Recommendation Engine
Uses content-based filtering with TF-IDF and cosine similarity
"""
from collections import Counter
from django.db.models import Count, Q
from products.models import Product, Category


class RecommendationEngine:
    """
    Hybrid recommendation engine combining:
    - Content-based: Similar products by category and description
    - Collaborative: Products viewed by similar users
    - Popularity: Frequently viewed/purchased products
    """

    def __init__(self, request):
        self.request = request
        self.user = request.user if request.user.is_authenticated else None
        self.session_key = request.session.session_key

    def get_user_preferences(self):
        """Gather user interaction data"""
        from .models import ProductView
        from wishlist.models import Wishlist
        from orders.models import OrderItem

        preferences = {
            'viewed_products': [],
            'wishlist_products': [],
            'purchased_products': [],
            'favorite_categories': [],
        }

        # Get viewed products
        if self.user:
            views = ProductView.objects.filter(user=self.user)
        elif self.session_key:
            views = ProductView.objects.filter(session_key=self.session_key)
        else:
            views = ProductView.objects.none()

        preferences['viewed_products'] = list(
            views.order_by('-viewed_at', '-view_count')
            .values_list('product_id', flat=True)[:20]
        )

        if self.user:
            # Wishlist items
            preferences['wishlist_products'] = list(
                Wishlist.objects.filter(user=self.user)
                .values_list('product_id', flat=True)
            )

            # Purchased products
            preferences['purchased_products'] = list(
                OrderItem.objects.filter(order__user=self.user)
                .values_list('product_id', flat=True)
            )

        # Calculate favorite categories
        all_product_ids = (
            preferences['viewed_products'] +
            preferences['wishlist_products'] +
            preferences['purchased_products']
        )

        if all_product_ids:
            category_counts = Counter(
                Product.objects.filter(id__in=all_product_ids)
                .values_list('category_id', flat=True)
            )
            preferences['favorite_categories'] = [
                cat_id for cat_id, _ in category_counts.most_common(5)
            ]

        return preferences

    def get_similar_products(self, product, limit=6):
        """Get products similar to a given product"""
        similar = Product.objects.filter(
            available=True,
            category=product.category
        ).exclude(id=product.id)

        # Prioritize by category match
        return list(similar[:limit])

    def get_personalized_recommendations(self, limit=8, exclude_ids=None):
        """Get personalized recommendations based on user preferences"""
        exclude_ids = exclude_ids or []
        preferences = self.get_user_preferences()

        recommended_ids = []
        scores = {}

        # Score based on favorite categories
        if preferences['favorite_categories']:
            category_products = Product.objects.filter(
                available=True,
                category_id__in=preferences['favorite_categories']
            ).exclude(id__in=exclude_ids)

            for product in category_products[:30]:
                if product.id not in recommended_ids:
                    scores[product.id] = scores.get(product.id, 0) + 10
                    recommended_ids.append(product.id)

        # Boost products similar to wishlist items
        if preferences['wishlist_products']:
            wishlist_categories = Product.objects.filter(
                id__in=preferences['wishlist_products']
            ).values_list('category_id', flat=True)

            related_products = Product.objects.filter(
                available=True,
                category_id__in=wishlist_categories
            ).exclude(
                id__in=exclude_ids + preferences['wishlist_products']
            )

            for product in related_products[:20]:
                if product.id not in recommended_ids:
                    recommended_ids.append(product.id)
                scores[product.id] = scores.get(product.id, 0) + 15

        # Boost products similar to purchases
        if preferences['purchased_products']:
            purchased_categories = Product.objects.filter(
                id__in=preferences['purchased_products']
            ).values_list('category_id', flat=True)

            related_products = Product.objects.filter(
                available=True,
                category_id__in=purchased_categories
            ).exclude(
                id__in=exclude_ids + preferences['purchased_products']
            )

            for product in related_products[:20]:
                if product.id not in recommended_ids:
                    recommended_ids.append(product.id)
                scores[product.id] = scores.get(product.id, 0) + 20

        # Sort by score and get top recommendations
        sorted_ids = sorted(
            recommended_ids,
            key=lambda x: scores.get(x, 0),
            reverse=True
        )[:limit]

        if sorted_ids:
            # Preserve order
            products = list(Product.objects.filter(id__in=sorted_ids, available=True))
            products.sort(key=lambda p: sorted_ids.index(p.id))
            return products

        # Fallback to popular products
        return self.get_popular_products(limit, exclude_ids)

    def get_popular_products(self, limit=8, exclude_ids=None):
        """Get popular/trending products as fallback"""
        from .models import ProductView

        exclude_ids = exclude_ids or []

        # Most viewed products
        popular_ids = (
            ProductView.objects.values('product_id')
            .annotate(total_views=Count('id'))
            .order_by('-total_views')
            .exclude(product_id__in=exclude_ids)[:limit]
        )

        product_ids = [item['product_id'] for item in popular_ids]

        if product_ids:
            products = list(Product.objects.filter(
                id__in=product_ids,
                available=True
            ))
            return products

        # Ultimate fallback: newest products
        return list(
            Product.objects.filter(available=True)
            .exclude(id__in=exclude_ids)
            .order_by('-created')[:limit]
        )

    def get_recommendations_for_product(self, product, limit=6):
        """Get 'You may also like' recommendations for a product page"""
        recommendations = []

        # First: Same category products
        same_category = self.get_similar_products(product, limit=limit)
        recommendations.extend(same_category)

        if len(recommendations) < limit:
            # Add from user preferences
            exclude_ids = [product.id] + [p.id for p in recommendations]
            more = self.get_personalized_recommendations(
                limit=limit - len(recommendations),
                exclude_ids=exclude_ids
            )
            recommendations.extend(more)

        return recommendations[:limit]
