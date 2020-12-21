from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.
User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True, default='photo.png')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Категория')
    slug = models.SlugField(max_length=255, verbose_name='url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ['title']  # сортирока по имяни в алф порядке


class Tag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']  # сортирока по имяни в алф порядке


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='url', unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    content = CKEditor5Field('Text', config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    photo = models.ImageField(blank=True, default='photo.png', verbose_name='Фото')
    comments = models.IntegerField(default=0, verbose_name='Кол-во комментариев')
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    category = models.ManyToManyField(Category, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name='Тег')

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # формирование ссылки 'posts' - name in urls
        return reverse('post', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Статью'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']  # сортирока по дате в обратном порядке от нового к старому
