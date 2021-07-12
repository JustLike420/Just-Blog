from django.shortcuts import render
from django.views.generic import CreateView
from .service import send
from .models import Contact
from .forms import ContactForm


# Create your views here.
class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact/tags/contact_tag.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        send(form.instance.email)
        return super().form_valid(form)
