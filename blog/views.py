from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, F
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin

from blog.models import Post, Category, Tag
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, PostCreateForm, CommentCreateForm
from django.contrib.auth import login, logout


# Work with user

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # вход после регистрации
            messages.success(request, 'registered')
            return redirect('/')
        else:
            messages.error(request, 'error')
    else:
        form = UserRegisterForm()

    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = UserLoginForm
    return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect('/')


# work with posts
class CreatePost(CreateView):
    form_class = PostCreateForm
    template_name = 'new_post.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect('home')


# def post_create(request):
#     form = PostCreateForm(request.POST or None, request.FILES or None)
#     author = request.user
#     if request.method == 'POST':
#         if form.is_valid():
#             form.instance.user = author
#             form.save()
#             return redirect('home')
#     else:
#         form = PostCreateForm()
#     return render(request, 'new_post.html', {'form': form})


class Home(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Blog'
        return context


class Get_Posts(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Blog'
        return context


class Get_Post(DetailView, FormMixin):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form_class = CommentCreateForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('post', kwargs={'slug': self.get_object().slug})

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = self.get_object()
        form.save()
        return super().form_valid(form)


# Search or filtered posts

class Search(ListView):
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context


class Post_By_Category(ListView):
    template_name = 'category.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class Post_By_Tag(ListView):
    template_name = 'tag.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context
