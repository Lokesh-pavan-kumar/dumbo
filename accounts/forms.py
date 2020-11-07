from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Profile,DumboUser


User = get_user_model()


class DumboUserLoginForm(forms.Form):
    identifier = forms.CharField(label='Username/Email')  # Users can enter either username or password to login
    # Since both username, email are unique for a user and can be used to identify them
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        identifier = self.cleaned_data.get('identifier')  # Get the identifier from the form data
        password = self.cleaned_data.get('password')  # Get the password from the form
        user_list = User.objects.filter(  # We use Q filtering to identify the user
            Q(username__iexact=identifier) | Q(email__iexact=identifier)
            # An `OR` operation to filter out the users that have entered their
            # username/email which will be used as an identifier
        ).distinct()
        # `user_list` is a queryset
        if not user_list.exists() and user_list.count != 1:
            # If the queryset doesn't exist or the list contains many users
            # We raise an error because only one user is supposed to exist
            # Most of the times the control reaches here only if the user_list doesn't exist
            raise forms.ValidationError("No account found with the given credentials")
        user_object = user_list.first()  # Get the user_object, can be used to display the user
        if not user_object.check_password(password):  # Check if the password can validate the user
            raise forms.ValidationError("The given combination of credentials are not correct")
        self.cleaned_data['user_object'] = user_object  # Add the user_object to the cleaned_data
        return super(DumboUserLoginForm, self).clean()


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = DumboUser
        fields = ['fullname', 'phone_number']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'twitter_link' ]