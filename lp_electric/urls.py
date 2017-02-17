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
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView

from lp_electric import views
from pages import urls as pages_urls
from pages.models import Page


catalog_urls = [
    url(r'^$', views.CategoryTree.as_view(), name='category_tree'),
    url(r'^categories/(?P<category_id>[0-9]+)/$',
        views.category_page, name='category'),
    url(r'^products/(?P<product_id>[0-9]+)/$',
        views.ProductPage.as_view(), name='product'),
    # url(r'^no-images/$', views.ProductsWithoutImages.as_view(),
    #     name='products_without_images'),
    # url(r'^no-text/$', views.ProductsWithoutText.as_view(),
    #     name='products_without_text'),
]

i18n_urlpatterns = i18n_patterns(
    url(r'^$', views.IndexPage.as_view(), name='index'),
    url(r'^catalog/', include(catalog_urls)),
    url(r'^pages/jobs/$', views.jobs, name='jobs'),
    url(r'^pages/', include(pages_urls)),
    url(r'^(?P<page>search)/$', views.Search.as_view(), name=Page.CUSTOM_PAGES_URL_NAME),
)

admin.autodiscover()

urlpatterns = [
    *i18n_urlpatterns,
    url(r'^admin/', admin.site.urls),
    url(r'^search/autocomplete/$', views.Autocomplete.as_view(), name='autocomplete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
