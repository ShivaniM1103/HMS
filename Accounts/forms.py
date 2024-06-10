
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class StaffSignUpForm(UserCreationForm):
    # username = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )
    # first_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )
    # last_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )
    # password1 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )
    # password2 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )
    # email = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )
    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','email','password1', 'password2', 'is_doctor', 'is_pharmacist')
        labels = {
            'password1':'Password',
            'password2':'Confirm Password',
        }


class SignUpForm(UserCreationForm):
    # username = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )
    # first_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )
    # last_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )
    # password1 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )
    # password2 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )
    # email = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )

    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','email','password1', 'password2')
        labels = {
            'password1':'Password',
            'password2':'Confirm Password',
        }

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['profile_pic', 'address','phoneno']
        labels = {
            'profile_pic': 'Profile Picture',
            'address': 'Address',
            'phoneno': 'Phone no.',
        }

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['profile_pic','department', 'address','phoneno']
        labels = {
            'profile_pic': 'Profile Picture',
            'address': 'Address',
            'department': 'Department',
            'phoneno': 'Phone no.',
        }

class PharmacistProfileForm(forms.ModelForm):
    class Meta:
        model = Pharmacist
        fields = ['profile_pic', 'address','phoneno']
        labels = {
            'profile_pic': 'Profile Picture',
            'address': 'Address',
            'phoneno': 'Phone no.',
        }

class DepartmentsForm(forms.ModelForm):
    class Meta:
        model = Departments
        fields = ['dname', 'description','phoneno']

class BedForm(forms.ModelForm):
    class Meta:
        model = Bed
        fields = ['Ebed','Gbed']
        labels = {
            'Ebed': 'Emergency Beds Count',
            'Gbed': 'General bed count',
        }