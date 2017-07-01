from django.db import models
from products.models import Products


class UserProducts(models.Model):
    PRODUCT_STATUS = (
        (1, 'In use'),
        (2, 'Returned'),
        (3, 'Redeemed')
    )
    user = models.ForeignKey(
        'appauth.AppUser',
        related_name='user_product'
    )
    product = models.ForeignKey(
        Products,
        related_name='product'
    )
    status = models.IntegerField(
        choices=PRODUCT_STATUS
    )
    added_on = models.DateTimeField(
        auto_now_add=True
    )

    @staticmethod
    def add(user, product):
        UserProducts(
            user=user,
            product=product,
            status=UserProducts.PRODUCT_STATUS[0][0]
        ).save()

