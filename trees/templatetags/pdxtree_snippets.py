"""
Re-usable snippets to provide a consistent look across templates
without repeating code.

Docs:
https://docs.djangoproject.com/en/1.8/howto/custom-template-tags/
"""

from django import template

register = template.Library()

@register.inclusion_tag('tree_cell.html')
def tree_cell(tree):
    """
    Standardize tree listings
    """
    return {'t': tree}
