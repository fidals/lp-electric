from modeltranslation.translator import translator, TranslationOptions
from pages.models import CustomPage, ModelPage, FlatPage, Page
from lp_electric.models import CategoryPage, ProductPage, Property


class PageTranslationOptions(TranslationOptions):
    fields = ('_title', 'h1', '_menu_title', 'content')


class PropertyTranslationOptions(TranslationOptions):
    fields = ('name', 'value')


class ModelTranslationOptions(TranslationOptions):
    fields = ('h1', 'content')

translator.register(Page, PageTranslationOptions)
translator.register(CustomPage, PageTranslationOptions)
translator.register(ModelPage, PageTranslationOptions)
translator.register(FlatPage, PageTranslationOptions)
translator.register(CategoryPage, ModelTranslationOptions)
translator.register(ProductPage, ModelTranslationOptions)
translator.register(Property, PropertyTranslationOptions)
