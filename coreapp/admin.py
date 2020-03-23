from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django.contrib.auth.hashers import check_password, make_password
from django import forms
from .models import User, Profile, Category, Tag, Article, Featured, Trending, Message, Advertisement, FAQ


# Register your models here.
class ProfileInline(admin.TabularInline):
    model = Profile


admin.site.register(Trending)
admin.site.register(Featured)
admin.site.register(Advertisement)


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
admin.site.register(FAQ)


class ArticleAdminForm(forms.ModelForm):
    details = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = '__all__'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    form = ArticleAdminForm


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
