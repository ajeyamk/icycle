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
    code = models.CharField(
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

    @staticmethod
    def calculate_count(status, ids):
        return Products.objects.filter(id__in=ids, category_id=status).count()
