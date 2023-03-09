from django import template

register = template.Library()

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

register.filter("usd", usd)