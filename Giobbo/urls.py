"""Giobbo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views, forms
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', LoginView.as_view(
        template_name="login.html",
        authentication_form=forms.UserLoginForm
    ), ),
    path('register/student', views.register_student),
    path('register/company', views.register_company),

    path('', views.home_view, name="home"),
    path('companies/', views.companies_list_view),
    path('companies/<int:company_id>', views.company_detail_view),
    path('companies/edit/<int:company_id>', views.company_edit_view, name="edit-company"),
    path('companies/manage/<int:company_id>', views.company_manage_internships, name="manage-company"),
    path('companies/add/<int:company_id>', views.company_add_internship, name="add-internship"),
    path('companies/delete/<int:company_id>/<int:internship_id>', views.company_delete_internship, name="delete-internship"),
    path('companies/update/<int:company_id>/<int:internship_id>', views.company_update_internship, name="update-internship"),

    path('students/', views.students_list_view),

    path('internships', views.internship_search_view)

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
