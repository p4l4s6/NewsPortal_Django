from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from coreapp.models import User, Message
from django.utils.translation import ugettext_lazy as _
from coreapp.models import Comment


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_pic']


class EmailAuthForm(AuthenticationForm):
    def clean(self):
        try:
            self.cleaned_data["username"] = get_user_model().objects.get(email=self.data["username"])
        except ObjectDoesNotExist:
            self.cleaned_data["username"] = "Email not found"
        return super(EmailAuthForm, self).clean()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['details', ]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
