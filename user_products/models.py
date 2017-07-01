from django.db import models

class UserProducts(models.Model):
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