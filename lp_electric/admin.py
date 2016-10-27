from django.contrib import admin
from lp_electric.models import Category, Product
from pages.models import ModelPage


# TODO - remove it
@admin.register(ModelPage)
class ModelPageAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
