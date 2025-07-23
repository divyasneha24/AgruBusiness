from django import forms
from django.contrib.auth.models import User
from .models import Profile
from farmers.models import FarmerCrop

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class CustomerFarmerRegistrationForm(forms.ModelForm):
    user_type = forms.ChoiceField(choices=Profile.USER_TYPE_CHOICES, widget=forms.RadioSelect)
    phone = forms.CharField(max_length=15, required=True)  # Add phone number field
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": ""})
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash password
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                user_type=self.cleaned_data['user_type'],
                phone=self.cleaned_data['phone'],  # Save phone number
            )
        return user


class FarmerCropForm(forms.ModelForm):
    class Meta:
        model = FarmerCrop
        fields = ['crop', 'price_per_kg']
