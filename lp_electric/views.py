"""
Shopelectro's search views.

NOTE: They all should be 'zero-logic'.
All logic should live in respective applications.
"""
from django.conf import settings

from catalog.views import catalog, search
from lp_electric.models import Category, Product

MODEL_MAP = {'product': Product, 'category': Category}


# --------- search -----------
class Search(search.Search):
    """Override model references to SE-specific ones."""
    model_map = MODEL_MAP
    template_path = 'search/{}.html'


class Autocomplete(search.Autocomplete):
    """Override model references to SE-specific ones."""
    model_map = MODEL_MAP
    see_all_label = settings.SEARCH_SEE_ALL_LABEL
    search_url = 'search'


# --------- catalog -----------
class CategoryTree(catalog.CategoryTree):
    """Override model attribute to SE-specific Category."""
    model = Category


class CategoryPage(catalog.CategoryPage):
    """
    Override model attribute to SE-specific Category.

    Extend get_context_data.
    """
    model = Category

    # def get_context_data(self, **kwargs):
    #     """Extended method. Add sorting options and view_types."""
    #     context = super(CategoryPage, self).get_context_data(**kwargs)
    #     category = self.get_object()
    #
    #     sorting = int(self.kwargs.get('sorting', 0))
    #     sorting_option = config.category_sorting(sorting)
    #
    #     # if there is no view_type specified, default will be tile
    #     view_type = self.request.session.get('view_type', 'tile')
    #     products, total_count = (
    #         category.get_recursive_products_with_count(sorting=sorting_option)
    #     )
    #
    #     return {
    #         **context,
    #         'products': products,
    #         'total_products': total_count,
    #         'sorting_options': config.category_sorting(),
    #         'sort': sorting,
    #         'view_type': view_type,
    #         'page': category.page,
    #     }


class ProductPage(catalog.ProductPage):
    """
    Override model attribute to SE-specific Product.

    Extend get_context_data.
    """
    model = Product

    # def get_context_data(self, **kwargs):
    #     """Extended method. Add product's images to context.."""
    #     context = super(ProductPage, self).get_context_data(**kwargs)
    #     product = self.get_object()
    #
    #     return {
    #         **context,
    #         'page': product.page,
    #     }
