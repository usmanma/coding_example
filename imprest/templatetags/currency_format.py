from django import template

register = template.Library()

@register.filter
def currency(amount):
    try:
        formatted_amount = "%0.2f" % float(amount)
    except ValueError:
        formatted_amount = amount

    return formatted_amount
