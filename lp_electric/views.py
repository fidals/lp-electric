"""
Shopelectro's search views.

NOTE: They all should be 'zero-logic'.
All logic should live in respective applications.
"""
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from catalog.views import catalog, search
from lp_electric.models import Category, Product
from pages.models import CustomPage

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

    def get(self, request):
        term = request.GET.get('term')

        products = Product.objects.filter(name__icontains=term).values_list('name')
        products = [product[0] for product in products]
        return JsonResponse(products, safe=False)


# --------- catalog -----------
class CategoryTree(catalog.CategoryTree):
    """Override model attribute to SE-specific Category."""
    model = Category


def category_page(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    children = category.get_children_sorted_by_position().values()
    for c in children:
        c['products'] = Category.objects.get(pk=c['id']).products.all()
    return render(request, 'category.html', {
        'category': category,
        'children': children,
        'page': category.page,
    })


class ProductPage(catalog.ProductPage):
    """
    Override model attribute to SE-specific Product.

    Extend get_context_data.
    """
    model = Product
    template_name = 'product.html'

    # def get_context_data(self, **kwargs):
    #     """Extended method. Add product's images to context.."""
    #     context = super(ProductPage, self).get_context_data(**kwargs)
    #     product = self.get_object()
    #
    #     return {
    #         **context,
    #         'page': product.page,
    #     }


def jobs(request):
    page = CustomPage.objects.get(slug='jobs')
    return render(request, 'jobs.html', {
        'page': page,
    })
