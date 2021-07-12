from django import template
from contact.forms import ContactForm

register = template.Library()


@register.inclusion_tag("contact/tags/contact_tag.html")
def contact_form():
    return {"contact_form": ContactForm()}
