from django.contrib import admin
from .models import User, Profile, Category, Tag, Article


# Register your models here.
class ProfileInline(admin.TabularInline):
    model = Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline, ]


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)
