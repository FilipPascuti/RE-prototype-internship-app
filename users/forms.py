from django import forms
from django.contrib.auth.forms import AuthenticationForm

from users.models import User, Internship
from users.utils import DomainTypes, WorkTypes


class CompanySignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'password']
        widgets = {'password': forms.PasswordInput()}

    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 8, "cols": 80}))
    confirm_password = forms.CharField(max_length=200, widget=forms.PasswordInput())
    domain = forms.ChoiceField(widget=forms.Select(), choices=DomainTypes.choices())
    contact_person = forms.CharField()
    location = forms.CharField(max_length=50)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            msg = "Passwords are not identical!"
            self.add_error('confirm_password', msg)


class StudentSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'password']
        widgets = {'password': forms.PasswordInput()}

    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 8, "cols": 80}))
    confirm_password = forms.CharField(max_length=200, widget=forms.PasswordInput())
    skills = forms.CharField(widget=forms.Textarea(attrs={"rows": 8, "cols": 80}))
    foreign_languages = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 8, "cols": 80}))
    personal_links = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 8, "cols": 80}))
    personal_projects = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 8, "cols": 80}))
    domain_of_interest = forms.ChoiceField(widget=forms.Select(), choices=DomainTypes.choices())
    profile_photo = forms.ImageField(required=False)
    cv = forms.FileField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            msg = "Passwords are not identical!"
            self.add_error('confirm_password', msg)


class CompanyEditForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=10)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 8, "cols": 80}))
    contact_person = forms.CharField(max_length=30)
    domain = forms.ChoiceField(widget=forms.Select(), choices=DomainTypes.choices())
    location = forms.CharField(max_length=50)


class CompanyAddInternshipForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 8, "cols": 80}))
    role_name = forms.CharField(widget=forms.Textarea(attrs={"rows": 1, "cols": 80}))
    duration = forms.CharField(widget=forms.Textarea(attrs={"rows": 1, "cols": 80}))
    date_expiration = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'date'}))
    letter_of_intent_needed = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    flexible_hours = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    remote_possibility = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    salary = forms.IntegerField(widget=forms.NumberInput(attrs={'min': '0'}))
    domain = forms.ChoiceField(widget=forms.Select(), choices=DomainTypes.choices())
    type = forms.ChoiceField(widget=forms.Select(), choices=WorkTypes.choices())
    location = forms.CharField(max_length=50)


class StudentEditForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=10)
    skills = forms.CharField(widget=forms.Textarea(attrs={"rows": 8, "cols": 80}))
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 8, "cols": 80}))
    foreign_languages = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 8, "cols": 80}))
    personal_links = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 8, "cols": 80}))
    personal_projects = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 8, "cols": 80}))
    domain_of_interest = forms.ChoiceField(widget=forms.Select(), choices=DomainTypes.choices())
    profile_photo = forms.ImageField(required=False)
    cv = forms.FileField(required=False)


class UserLoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': "Email", 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Parola', 'class': 'form-control'}))
