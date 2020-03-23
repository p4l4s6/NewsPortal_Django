import itertools
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import Count
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from .MyUserManager import MyUserManager
from django.urls import reverse
from coreapp.utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save

from .utils import unique_slug_generator
from coreapp.utils import POLL_ANSWER


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    email = models.EmailField(unique=True, null=True)
    profile_pic = models.ImageField(default='media/user/default_user_image.png', upload_to='user/')
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_superuser = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as superuser. '
            'Select this to allow all access'
        ),
    )
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.first_name)


class Category(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField(default='', editable=False, max_length=100)
    is_active = models.BooleanField(null=False, default=True)
    thumbnail = models.ImageField(default='media/category/default.png', upload_to='category/')

    is_menu = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


pre_save.connect(pre_save_receiver, sender=Category)


class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False, blank=False)
    details = models.TextField(max_length=3000, null=False, blank=False)
    thumbnail = models.ImageField(default='media/article/default.png', upload_to='article/')
    tag = models.ManyToManyField(Tag)
    is_published = models.BooleanField(default=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(default='', editable=False, max_length=150)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def summary(self):
        return self.details[:100]

    def get_related_posts_by_tags(self):
        return Article.objects.filter(tag__in=self.tag.all())[:3]


pre_save.connect(pre_save_receiver, sender=Article)


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.TextField(max_length=400, null=False, blank=False)
    rating = models.IntegerField(default=3, null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.details

    def get_full_star(self):
        return range(1, self.rating)

    def get_empty_star(self):
        return range(1, 5 - self.rating)


class Featured(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.article.title


class Trending(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.article.title


class Advertisement(models.Model):
    name = models.CharField(max_length=50, help_text="Ad Campaign Name", null=False, blank=False)

    banner_1 = models.ImageField(upload_to='ad/', default='ad/default_banner_ad.jpg')
    banner_1_url = models.CharField(max_length=100, null=True, blank=True)
    banner_2 = models.ImageField(upload_to='ad/', default='ad/default_banner_ad.jpg')
    banner_2_url = models.CharField(max_length=100, null=True, blank=True)
    banner_3 = models.ImageField(upload_to='ad/', default='ad/default_banner_ad.jpg')
    banner_3_url = models.CharField(max_length=100, null=True, blank=True)
    banner_4 = models.ImageField(upload_to='ad/', default='ad/default_banner_ad.jpg')
    banner_4_url = models.CharField(max_length=100, null=True, blank=True)

    right_square_1 = models.ImageField(upload_to='ad/', default='ad/default_square_ad.jpg')
    square_1_url = models.CharField(max_length=100, null=True, blank=True)
    right_square_2 = models.ImageField(upload_to='ad/', default='ad/default_square_ad.jpg')
    square_2_url = models.CharField(max_length=100, null=True, blank=True)
    right_square_3 = models.ImageField(upload_to='ad/', default='ad/default_square_ad.jpg')
    square_3_url = models.CharField(max_length=100, null=True, blank=True)
    right_square_4 = models.ImageField(upload_to='ad/', default='ad/default_square_ad.jpg')
    square_4_url = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


# class Poll(models.Model):
#     question = models.CharField(max_length=150, null=False, blank=False)
#     option_1 = models.CharField(max_length=100, null=False, blank=False)
#     option_2 = models.CharField(max_length=100, null=False, blank=False)
#     answer = models.CharField(choices=POLL_ANSWER, null=False, blank=False)

class Message(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.CharField(max_length=100, null=False, blank=False)
    subject = models.CharField(max_length=100, null=False, blank=False)
    message = models.TextField(max_length=600, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FAQ(models.Model):
    question = models.CharField(max_length=100, null=False, blank=False)
    answer = models.TextField(max_length=600, null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
