from django import template
from django.core.urlresolvers import resolve, reverse
from lp_electric.models import Category

register = template.Library()


@register.assignment_tag
def roots():
    return Category.objects.root_nodes().order_by('page__position')


@register.assignment_tag
def resolve_url(request):
    return resolve(request.path_info)


@register.assignment_tag
def translated_path(request, resolve_match):
    url_name = (
        (resolve_match.namespace + ':')
        if resolve_match.namespace else '' +
        resolve_match.url_name
    )
    return reverse(url_name, args=resolve_match.args, kwargs=resolve_match.kwargs)
