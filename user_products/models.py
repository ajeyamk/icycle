from django.db import models
from products.models import Products


class UserProducts(models.Model):
    user = models.ForeignKey(
        'appauth.AppUser',
        related_name='user_product'
    )
    product = models.ForeignKey(
        Products,
        related_name='product'
    )
    added_on = models.DateTimeField(
        auto_now_add=True
    )

    @staticmethod
    def add(user, product):
        UserProducts(
            user=user,
            product=product
        ).save()
