from django.db import models
from appauth.models import AppUser
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

    @staticmethod
    def calculate_user_points(user_product):
        # Categories.objects.get(id=product.categories)
        refundable_amount = user_product.product.category.refundable_amount
        user = AppUser.objects.get(id=user_product.user.id)
        new_user_point = user.user_point + refundable_amount
        user.user_point = new_user_point
        user.save()
        return new_user_point
