from django import template
from lp_electric.models import Category

register = template.Library()


@register.assignment_tag
def roots():
    return Category.objects.root_nodes().order_by('page__position')
