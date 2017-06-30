from django.db import models


class Categories(models.Model):
    CATEGORY_TYPES = (
        (1, 'Plastic Bottle'),
        (2, 'Carry bags'),
        (3, 'Containers')
    )
    name = models.CharField(
        max_length=255,
        blank=True
    )
    type = models.IntegerField(
        choices=CATEGORY_TYPES
    )
    refundable_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.0
    )
    added_on = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
