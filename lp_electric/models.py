from django.db import models
from django.core.urlresolvers import reverse

from catalog.models import AbstractProduct, AbstractCategory


class Category(AbstractCategory):
    """
    SE-specific Category model.

    Define product_relation class attribute to make use of
    get_recursive_products_with_count method in its abstract
    superclass.
    """
    product_relation = 'products'

    def get_absolute_url(self):
        """Return url for model."""
        return reverse('category', args=(self.id,))


class Product(AbstractProduct):
    """
    SE-specific Product model.

    Define n:1 relation with SE-Category and 1:n with Property.
    Add wholesale prices.
    """

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=None,
        related_name='products', db_index=True
    )

    def get_absolute_url(self):
        return reverse('product', args=(self.id,))
