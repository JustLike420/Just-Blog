from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import Post


class Home(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Blog'
        return context


def blog(request):
    return render(request, 'blog.html', {})


def post(request):
    return render(request, 'post.html', {})
