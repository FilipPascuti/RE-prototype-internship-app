import logging

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from .forms import StudentSignUpForm, CompanySignUpForm, CompanyEditForm, CompanyAddInternshipForm
from .models import Company, Student, User, Location, Internship, Application, ApplicationStatus
from django.forms.models import model_to_dict
from django.db.models import Q


def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)


def companies_list_view(request, *args, **kwargs):
    companies_list = Company.objects.all()
    context = {
        'companies_list': companies_list
    }
    return render(request, "users/companies/companies_list.html", context, status=200)


def company_detail_view(request, company_id, *args, **kwargs):
    try:
        company = Company.objects.get(id=company_id)
    except:
        raise Http404
    context = {
        'company': company
    }
    return render(request, "pages/details/company_details.html", context, status=200)


def students_list_view(request, *args, **kwargs):
    students_list = Student.objects.all()
    context = {
        'students_list': students_list
    }
    return render(request, "users/students/students_list.html", context, status=200)


def register_student(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            doc = request.FILES
            user_instance = form.save(commit=False)
            user_instance.is_student = True
            user_instance.set_password(form.cleaned_data['password'])
            user_instance.description = form.cleaned_data['description']
            user_instance.save()
            domain_of_interest = form.cleaned_data['domain_of_interest']
            skills = form.cleaned_data['skills']
            personal_projects = form.cleaned_data['personal_projects']
            foreign_languages = form.cleaned_data['foreign_languages']
            personal_links = form.cleaned_data['personal_links']
            profile_photo, cv = None, None
            if doc:
                profile_photo = doc['profile_photo']
                cv = doc['cv']
            student = Student(user=user_instance, domain_of_interest=domain_of_interest, skills=skills,
                              personal_projects=personal_projects, foreign_languages=foreign_languages,
                              personal_links=personal_links, profile_photo=profile_photo, cv=cv)
            student.save()
            return redirect("/")
    else:
        form = StudentSignUpForm()
    context = {'form': form}
    return render(request, "registration/student_sign_up.html", context=context)


def register_company(request):
    if request.method == 'POST':
        form = CompanySignUpForm(request.POST)
        if form.is_valid():
            user_instance = form.save(commit=False)
            user_instance.is_company = True
            user_instance.set_password(form.cleaned_data['password'])
            user_instance.description = form.cleaned_data['description']
            user_instance.save()
            domain = form.cleaned_data['domain']
            contact_person = form.cleaned_data['contact_person']
            location_name = form.cleaned_data['location']

            new_location, created = Location.objects.get_or_create(name=location_name)
            if created:
                new_location.save()

            company = Company(user=user_instance, domain=domain, contact_person=contact_person, location=new_location)
            company.save()
            return redirect("/")
    else:
        form = CompanySignUpForm()
    context = {'form': form}
    return render(request, "registration/company_sign_up.html", context=context)


def company_to_dictionary(company):
    company_dict = model_to_dict(company, fields=["domain", "contact_person"])
    user_dict = model_to_dict(company.user, fields=["email", "name", "description", "phone"])
    company_dict.update(user_dict)
    company_dict.update({"location": company.location.name})
    return company_dict


def company_edit_view(request, company_id, *args, **kwargs):
    try:
        company = Company.objects.get(id=company_id)
        user = User.objects.get(email=company.user)
        location = Location.objects.get(id=company.location.id)
    except:
        raise Http404
    if request.method == 'POST':
        form = CompanyEditForm(request.POST)
        if form.is_valid():
            company.contact_person = form.cleaned_data['contact_person']
            company.domain = form.cleaned_data['domain']
            company.user.name = form.cleaned_data['name']
            company.user.phone = form.cleaned_data['phone']
            company.user.description = form.cleaned_data['description']

            if form.cleaned_data['location'] != company.location.name:  # new location given
                new_location, created = Location.objects.get_or_create(name=form.cleaned_data['location'])
                if created:
                    new_location.save()
                company.location = new_location

            company.save()
            company.user.save()
            return redirect("/")
    else:
        company_dict = company_to_dictionary(company)
        form = CompanyEditForm(initial=company_dict)
    context = {'form': form}
    return render(request, "pages/details/company_update_details.html", context=context)


def company_manage_internships(request, company_id, *args, **kwargs):
    try:
        company = Company.objects.get(id=company_id)
    except:
        raise Http404
    company_internship_list = Internship.objects.all().filter(company=company)

    context = {
        'company_internship_list': company_internship_list,
        'company': company
    }
    return render(request, "pages/company/internship_dashboard.html", context, status=200)


def company_delete_internship(request, company_id, internship_id, *args, **kwargs):
    try:
        internship = Internship.objects.get(id=internship_id)
    except:
        raise Http404

    Internship.objects.filter(id=internship_id).delete()
    return redirect("/companies/manage/{}".format(str(company_id)))


def internship_to_dict(internship):
    internship_dict = model_to_dict(internship, fields=["active,"
                                                        "role_name",
                                                        "description", "date_posted", "date_expiration",
                                                        "letter_of_intent_needed", "flexible_hours",
                                                        "remote_possibility", "duration",
                                                        "salary", "paid", "domain", "type"])

    return internship_dict


def company_update_internship(request, company_id, internship_id, *args, **kwargs):
    try:
        company = Company.objects.get(id=company_id)
        internship = Internship.objects.get(id=internship_id)
    except:
        raise Http404
    if request.method == 'POST':
        form = CompanyAddInternshipForm(request.POST)
        if form.is_valid():
            role_name = form.cleaned_data['role_name']
            description = form.cleaned_data['description']
            domain = form.cleaned_data['domain']
            date_expiration = form.cleaned_data['date_expiration']
            type = form.cleaned_data['type']
            remote_possibility = form.cleaned_data['remote_possibility']
            flexible_hours = form.cleaned_data['flexible_hours']
            letter_of_intent_needed = form.cleaned_data['letter_of_intent_needed']
            salary = form.cleaned_data['salary']
            location_name = form.cleaned_data['location']

            if form.cleaned_data['location'] != company.location.name:  # new location given
                new_location, created = Location.objects.get_or_create(name=form.cleaned_data['location'])
                if created:
                    new_location.save()

            Internship.objects.filter(id=internship_id).update(role_name=role_name, description=description,
                                                               domain=domain,
                                                               type=type, flexible_hours=flexible_hours,
                                                               remote_possibility=remote_possibility,
                                                               letter_of_intent_needed=letter_of_intent_needed,
                                                               date_expiration=date_expiration,
                                                               salary=salary, location=new_location, active=True,
                                                               company=company)
            return redirect("/companies/manage/{}".format(str(company_id)))
    else:
        internship_dict = internship_to_dict(internship)
        form = CompanyAddInternshipForm(initial=internship_dict)

    context = {
        'form': form,
        'company': company
    }
    return render(request, "pages/internship/add_internship.html", context=context, status=200)


def company_add_internship(request, company_id, *args, **kwargs):
    try:
        company = Company.objects.get(id=company_id)
    except:
        raise Http404

    if request.method == 'POST':
        form = CompanyAddInternshipForm(request.POST)
        if form.is_valid():
            role_name = form.cleaned_data['role_name']
            description = form.cleaned_data['description']
            domain = form.cleaned_data['domain']
            date_expiration = form.cleaned_data['date_expiration']
            type = form.cleaned_data['type']
            remote_possibility = form.cleaned_data['remote_possibility']
            flexible_hours = form.cleaned_data['flexible_hours']
            letter_of_intent_needed = form.cleaned_data['letter_of_intent_needed']
            salary = form.cleaned_data['salary']
            location_name = form.cleaned_data['location']

            new_location, created = Location.objects.get_or_create(name=location_name)
            if created:
                new_location.save()
            internship = Internship(role_name=role_name, description=description, domain=domain,
                                    type=type, flexible_hours=flexible_hours, remote_possibility=remote_possibility,
                                    letter_of_intent_needed=letter_of_intent_needed, date_expiration=date_expiration,
                                    salary=salary, location=new_location, active=True)
            internship.company = company
            internship.save()
            return redirect("/companies/manage/{}".format(str(company_id)))
    else:
        form = CompanyAddInternshipForm()

    context = {
        'form': form,
        'company': company
    }
    return render(request, "pages/internship/add_internship.html", context=context, status=200)


def internship_search_view(request, student_id, *args, **kwargs):
    student = Student.objects.get(id=student_id)

    internships_list = Internship.objects.all()

    internships_applied = set()
    for application in Application.objects.filter(student=student):
        internships_applied.add(application.internship)

    internships = []

    for internship in internships_list:
        if internship in internships_applied:
            internships.append([internship, True])
        else:
            internships.append([internship, False])

    context = {
        'internships_list': internships
    }
    return render(request, "users/internships/internships_search.html", context, status=200)


def apply_to_internship(request, internship_id, student_id, *args, **kwargs):
    internship = Internship.objects.get(id=internship_id)
    student = Student.objects.get(id=student_id)

    application = Application(internship=internship, student=student, status=ApplicationStatus.choices()[0][0])
    application.save()

    return redirect("/internships/{}".format(str(student_id)))


def company_see_applicants(request, company_id, *args, **kwargs):

    company = Company.objects.get(id=company_id)

    internships = Internship.objects.filter(company=company)

    applications = Application.objects.filter(internship__in=internships)

    print(applications)

    context = {
        'applications': applications
    }

    return render(request, "pages/company/see_aplicants.html", context=context, status=200)
