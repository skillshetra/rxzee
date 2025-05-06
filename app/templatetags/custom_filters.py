from django import template
register = template.Library()
@register.filter
def condition_link(value, *args):
    if isinstance(value, str):
        return value.replace(' ', '-')
    return value
@register.filter
def length(value, *args):
    return len(value)
@register.filter
def drug_name(value, *args):
    if isinstance(value, str):
        if len(value) > 30:
            return value[:30] + "..."
    return value
@register.filter
def generic_name(value, *args):
    if isinstance(value, str):
        return value.replace('|', ', ')
    return value
@register.filter
def get_generic_name(value, *args):
    if isinstance(value, str):
        return ', '.join(value.replace(')', '').split('(')[1:]).replace(' ', '-')
    return value
@register.filter
def zip_lists(list1, list2):
    return zip(list1, list2)
@register.filter
def slice_items(value, args):
    """Returns a sliced list based on start and end."""
    try:
        if ':' in args:
            start, end = args.split(':')
            start = int(start) if start else 0
            end = int(end) if end else None
        else:
            start = int(args)
            end = None
            
        return value[start:end]
    except (ValueError, TypeError):
        return value