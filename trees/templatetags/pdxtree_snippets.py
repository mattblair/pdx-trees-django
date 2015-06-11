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


@register.inclusion_tag('map_div_headers.html')
def map_div_headers():
    return {}


@register.inclusion_tag('map_div_js.html', takes_context=True)
def map_div_js(context, center_latitude, center_longitude, zoom_level, map_div_id):
    """
    Standardize map display
    
    zoom_level should be 14 or higher for individual trees.
    map_div_id may be: map or tree-map
    """
    return {
        'geojson': context['geojson'],
        'zoom_level': zoom_level,
        'center_latitude': center_latitude,
        'center_longitude': center_longitude,
        'map_div_id': map_div_id
    }


@register.inclusion_tag('supplemental_content_div.html')
def supplemental_div(content):
    """
    Standardize supplemental content listings
    
    Might not be possible if genus and tree content diverge
    """
    return {'c': content}
