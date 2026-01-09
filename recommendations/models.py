from django.db import models
from django.conf import settings
from products.models import Product


class ProductView(models.Model):
    """Track product views for recommendation engine"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=1)

    class Meta:
        # One record per user/session + product combination
        unique_together = [
            ('user', 'product'),
            ('session_key', 'product'),
        ]
        ordering = ['-viewed_at']

    def __str__(self):
        identifier = self.user.username if self.user else f"Guest:{self.session_key[:8]}"
        return f"{identifier} viewed {self.product.name}"
