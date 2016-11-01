from django.db import models
from django.core.urlresolvers import reverse

from catalog.models import AbstractProduct, AbstractCategory
from pages.models import PageMixin, ModelPage, Page


class Category(AbstractCategory, PageMixin):
    """
    SE-specific Category model.

    Define product_relation class attribute to make use of
    get_recursive_products_with_count method in its abstract
    superclass.
    """
    product_relation = 'products'

    @property
    def products(self):
        return Product.objects.get_products_by_category(self)

    def get_absolute_url(self):
        """Return url for model."""
        return reverse('category', args=(self.id,))


class Product(AbstractProduct, PageMixin):
    """
    SE-specific Product model.

    Define n:1 relation with SE-Category and 1:n with Property.
    Add wholesale prices.
    """

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=None,
        related_name='products', db_index=True
    )

    sibling = models.ForeignKey(
        'Product', on_delete=models.DO_NOTHING, null=True, blank=True,
        related_name='siblings', db_index=True
    )

    def get_absolute_url(self):
        return reverse('product', args=(self.id,))

    def save(self, *args, **kwargs):
        if self.sibling == self:
            self.sibling = None
        super(Product, self).save(*args, **kwargs)
        if self.sibling and self.sibling.sibling != self:
            self.sibling.sibling = self
            self.sibling.save()


def create_model_page_managers(*args: [models.Model]):
    """Create managers for dividing ModelPage entities"""
    def is_correct_arg(arg):
        return isinstance(arg, type(models.Model))

    assert all(map(is_correct_arg, args)), 'args should be ModelBase type'

    def create_manager(model):
        class ModelPageManager(models.Manager):
            def get_queryset(self):
                return super(ModelPageManager, self).get_queryset().filter(
                    related_model_name=model._meta.db_table)
        return ModelPageManager

    return [create_manager(model) for model in args]


CategoryPageManager, ProductPageManager = create_model_page_managers(Category, Product)


class CategoryPage(ModelPage):
    """Create proxy model for Admin"""
    class Meta(ModelPage.Meta):
        proxy = True

    objects = CategoryPageManager()


class ProductPage(ModelPage):
    """Create proxy model for Admin"""
    class Meta(ModelPage.Meta):
        proxy = True

    objects = ProductPageManager()


class Property(models.Model):

    name = models.CharField(max_length=255)
    value = models.CharField(max_length=500)

    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, default=None,
        related_name='properties', db_index=True
    )
