from django.contrib import admin
from .models import Student, Company, Internship, Location, Application, WorkExperience, AcademicExperience

admin.site.register(Location)
admin.site.register(Company)
admin.site.register(Student)
admin.site.register(Internship)
admin.site.register(Application)
admin.site.register(WorkExperience)
admin.site.register(AcademicExperience)

