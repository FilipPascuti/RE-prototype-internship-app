from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from .managers import UserManager
from .utils import DomainTypes, WorkTypes, ApplicationStatus, Degree


class Location(models.Model):
    name = models.CharField(max_length=50)


class User(AbstractBaseUser, PermissionsMixin):
    is_student = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    description = models.TextField()
    phone = models.CharField(max_length=10)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student')
    domain_of_interest = models.IntegerField(choices=DomainTypes.choices(), default=DomainTypes.IT)
    skills = models.TextField()
    personal_projects = models.TextField(null=True, blank=True)
    foreign_languages = models.TextField(null=True, blank=True)
    personal_links = models.TextField(null=True, blank=True)
    profile_photo = models.ImageField(null=True, blank=True, upload_to='media/students/photos')
    cv = models.FileField(null=True, blank=True, upload_to='media/students/cvs')

    def get_domain_type_label(self):
        return DomainTypes(self.domain_of_interest).name.title()

    def __str__(self):
        return self.user.email


class Company(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company')
    domain = models.IntegerField(choices=DomainTypes.choices(), default=DomainTypes.IT)
    contact_person = models.CharField(max_length=30)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def get_domain_type_label(self):
        return DomainTypes(self.domain).name.title()

    def __str__(self):
        return self.user.email


class Internship(models.Model):
    active = models.BooleanField(default=False)
    role_name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    date_posted = models.DateTimeField(default=now)
    date_expiration = models.DateTimeField()
    letter_of_intent_needed = models.BooleanField(default=False)
    flexible_hours = models.BooleanField(default=False)
    remote_possibility = models.BooleanField(default=False)
    duration = models.CharField(max_length=50)
    salary = models.FloatField()
    paid = models.BooleanField(default=True)

    domain = models.IntegerField(choices=DomainTypes.choices(), default=DomainTypes.IT)
    type = models.CharField(max_length=50, choices=WorkTypes.choices(), default=WorkTypes.FULL_TIME)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def get_domain_type_label(self):
        return DomainTypes(self.domain).name.title()


class Application(models.Model):
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=ApplicationStatus.choices(), default=ApplicationStatus.RECEIVED_CV)


class Experience(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    institution = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class AcademicExperience(Experience):
    field = models.CharField(max_length=50)
    degree = models.CharField(max_length=50, choices=Degree.choices(), default=Degree.OTHER)


class WorkExperience(Experience):
    position = models.CharField(max_length=50)
    description = models.CharField(max_length=50, default="")
