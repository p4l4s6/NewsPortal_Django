from django.contrib import admin
from django.contrib.auth.hashers import check_password, make_password

from .models import User, Profile, Category, Tag, Article


# Register your models here.
class ProfileInline(admin.TabularInline):
    model = Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline, ]

    def save_model(self, request, obj, form, change):
        user_database = User.objects.get(pk=obj.pk)
        if not (check_password(form.data['password'], user_database.password) or user_database.password == form.data[
            'password']):
            obj.password = make_password(obj.password)
        else:
            obj.password = user_database.password
        super().save_model(request, obj, form, change)


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)
