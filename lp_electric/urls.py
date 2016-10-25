"""lp_electric URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView

from lp_electric.views import Autocomplete, Search


catalog_urls = [
    # url(r'^$', catalog.CategoryTree.as_view(), name='category_tree'),
    # url(r'^categories/(?P<slug>[\w-]+)/$',
    #     catalog.CategoryPage.as_view(), name='category'),
    # url(r'^categories/(?P<slug>[\w-]+)/(?P<sorting>[0-9]*)/$',
    #     catalog.CategoryPage.as_view(), name='category'),
    # url(r'categories/(?P<category_slug>[\w-]+)/load-more/'
    #     r'(?P<offset>[0-9]+)/(?P<sorting>[0-9]*)/$',
    #     catalog.load_more, name='load_more'),
    # url(r'^products/(?P<product_id>[0-9]+)/$',
    #     catalog.ProductPage.as_view(), name='product'),
    # url(r'^no-images/$', catalog.ProductsWithoutImages.as_view(),
    #     name='products_without_images'),
    # url(r'^no-text/$', catalog.ProductsWithoutText.as_view(),
    #     name='products_without_text'),
]

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^admin/', admin.site.urls),
    url(r'^catalog/', include(catalog_urls)),
    url(r'^search/autocomplete/$', Autocomplete.as_view(), name='autocomplete'),
    url(r'^search/$', Search.as_view(), name='search'),
]
