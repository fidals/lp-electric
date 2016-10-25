"""
Shopelectro's search views.

NOTE: They all should be 'zero-logic'.
All logic should live in respective applications.
"""
from django.conf import settings

from catalog.views import search
from lp_electric.models import Category, Product

MODEL_MAP = {'product': Product, 'category': Category}


class Search(search.Search):
    """Override model references to SE-specific ones."""
    model_map = MODEL_MAP
    template_path = 'search/{}.html'


class Autocomplete(search.Autocomplete):
    """Override model references to SE-specific ones."""
    model_map = MODEL_MAP
    see_all_label = settings.SEARCH_SEE_ALL_LABEL
    search_url = 'search'
