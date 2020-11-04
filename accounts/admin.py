from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import DumboUser,Profile


# Register your models here.

class DumboUserCreationForm(forms.ModelForm):
    """A Form for creating DumboUser"""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    # fullname = forms.CharField(label='Full Name', required=False)
    phone_number = forms.CharField(label='Phone Number', required=False)

    class Meta:
        model = DumboUser
        fields = ['username', 'email', 'fullname', 'phone_number']
        required = ['username', 'email']

    def clean_password2(self):
        # Check that the two password entries match and validate
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match')
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class DumboUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = DumboUser
        fields = ['email', 'password', 'fullname', 'phone_number', 'is_active', 'is_superuser']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class DumboUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = DumboUserChangeForm
    add_form = DumboUserCreationForm

    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'fullname')  # The fields that will be displayed in the Admin Panel.
    list_filter = ('is_superuser', 'is_staff')  # Filters available
    fieldsets = (
        ('Authentication Info', {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('fullname', 'phone_number', )}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute.
    # UserAdmin overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'fullname', 'phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'username', 'fullname')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(DumboUser, DumboUserAdmin)
admin.site.register(Profile)
admin.site.unregister(Group)
