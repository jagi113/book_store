from django import template

register = template.Library()


@register.filter
def batch(l, n):
    """
    Batch a list into sublists of size n.
    """
    n = int(n)
    return [l[i : i + n] for i in range(0, len(l), n)]


@register.filter
def splitandbreak(value, character):
    results = [val.strip() + "<br>" for val in value.split(character)]
    return results
