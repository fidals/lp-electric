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
def reverse_url(resolve_match):
    m = resolve_match
    url_name = (
        m.namespace + ':' + m.url_name
        if m.namespace
        else m.url_name
    )
    return reverse(url_name, args=m.args, kwargs=m.kwargs)
