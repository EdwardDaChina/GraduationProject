from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.db import models


class Author(models.Model):  # 商品品类模型
    name = models.CharField('Author', max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'author'
        verbose_name_plural = 'author'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('rs:product_list_by_author', args=[self.slug])


class Genre(models.Model):  # 商品品类模型
    name = models.CharField('Genre', max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'genre'
        verbose_name_plural = 'genre'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('rs:product_list_by_genre', args=[self.slug])


class Cover(models.Model):  # 商品品类模型
    name = models.CharField('cover', max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'cover'
        verbose_name_plural = 'cover'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('rs:product_list_by_cover', args=[self.slug])


class Publication(models.Model):  # 商品品类模型
    name = models.CharField('publication', max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'publication'
        verbose_name_plural = 'publication'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('rs:product_list_by_publication', args=[self.slug])


class Product(models.Model):
    genre = models.ForeignKey(Genre, related_name='genre', on_delete=models.CASCADE)
    cover = models.ForeignKey(Cover, related_name='cover', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    author = models.ForeignKey(Author, related_name='author', on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, related_name='publication', on_delete=models.CASCADE)
    ISBN = models. CharField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    pubtime = models.DateField(default=timezone.now)

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('rs:product_detail', args=[self.id, self.slug])


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user/%Y/%m/%d/', blank=True)

    def __str__(self):
        return "Profile for user {}".format(self.user.username)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    review = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()  # 默认的管理器
    published = PublishedManager()  # 自定义管理器

    def get_absolute_url(self):
        return reverse('rs:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Meta:
        ordering = ('-publish',)


def __str__(self):
    return self.title


