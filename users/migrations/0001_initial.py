# Generated by Django 2.2 on 2021-01-10 11:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.managers
import users.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_student', models.BooleanField(default=False)),
                ('is_company', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('phone', models.CharField(max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', users.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.IntegerField(choices=[(1, 'IT'), (2, 'MEDICAL'), (3, 'TOURISM')], default=users.utils.DomainTypes(1))),
                ('contact_person', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=50)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='AcademicExperience',
            fields=[
                ('experience_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.Experience')),
                ('field', models.CharField(max_length=50)),
                ('degree', models.CharField(choices=[('HIGH_SCHOOL_DIPLOMA', 'HIGH_SCHOOL_DIPLOMA'), ('BACHELORS_DEGREE', 'BACHELORS_DEGREE'), ('MASTERS_DEGREE', 'MASTERS_DEGREE'), ('DOCTORAL_DEGREE', 'DOCTORAL_DEGREE'), ('OTHER', 'OTHER')], default=users.utils.Degree('OTHER'), max_length=50)),
            ],
            bases=('users.experience',),
        ),
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('experience_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.Experience')),
                ('position', models.CharField(max_length=50)),
                ('description', models.CharField(default='', max_length=50)),
            ],
            bases=('users.experience',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_of_interest', models.IntegerField(choices=[(1, 'IT'), (2, 'MEDICAL'), (3, 'TOURISM')], default=users.utils.DomainTypes(1))),
                ('skills', models.TextField()),
                ('personal_projects', models.TextField(blank=True, null=True)),
                ('foreign_languages', models.TextField(blank=True, null=True)),
                ('personal_links', models.TextField(blank=True, null=True)),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Internship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('role_name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_expiration', models.DateTimeField()),
                ('letter_of_intent_needed', models.BooleanField(default=False)),
                ('flexible_hours', models.BooleanField(default=False)),
                ('remote_possibility', models.BooleanField(default=False)),
                ('duration', models.CharField(max_length=50)),
                ('salary', models.FloatField()),
                ('paid', models.BooleanField(default=True)),
                ('domain', models.IntegerField(choices=[(1, 'IT'), (2, 'MEDICAL'), (3, 'TOURISM')], default=users.utils.DomainTypes(1))),
                ('type', models.CharField(choices=[('PART_TIME', 'PART_TIME'), ('FULL_TIME', 'FULL_TIME')], default=users.utils.WorkTypes('FULL_TIME'), max_length=50)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Company')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Location')),
            ],
        ),
        migrations.AddField(
            model_name='experience',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Student'),
        ),
        migrations.AddField(
            model_name='company',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Location'),
        ),
        migrations.AddField(
            model_name='company',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('RECEIVED_CV', 'RECEIVED_CV'), ('HR_INTERVIEW', 'HR_INTERVIEW'), ('TECHNICAL_INTERVIEW', 'TECHNICAL_INTERVIEW'), ('ACCEPTED', 'ACCEPTED'), ('REJECTED', 'REJECTED')], default=users.utils.ApplicationStatus('RECEIVED_CV'), max_length=50)),
                ('internship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Internship')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Student')),
            ],
        ),
    ]
