from django.db import models
from product_categories.models import Categories


class Products(models.Model):
    category = models.ForeignKey(
        Categories,
        related_name='category_type'
    )
    is_active = models.BooleanField(
        default=True
    )
    account_uuid = models.CharField(
        max_length=255,
        null=True
    )
    added_on = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name