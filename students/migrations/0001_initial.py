import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import students.managers
import students.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('type', models.CharField(blank=True, choices=[('student', 'Student'), ('teacher', 'Teacher'), ('mentor', 'Mentor')], max_length=60)),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether this user can log into the admin site.', verbose_name='staff')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', students.managers.CustomManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=14, null=True, unique=True, validators=[django.core.validators.RegexValidator('\\d{10,14}')])),
                ('birthdate', models.DateField(blank=True, default=datetime.date.today, null=True, validators=[students.validators.older_than_18])),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatar')),
                ('resume', models.FileField(blank=True, null=True, upload_to='resume')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_course', to='courses.course')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('first_name', models.CharField(max_length=60, validators=[django.core.validators.MinLengthValidator(2)])),
                ('last_name', models.CharField(max_length=80, validators=[django.core.validators.MinLengthValidator(2)])),
                ('email', models.EmailField(blank=True, max_length=120, null=True, validators=[students.validators.no_elon_validator, students.validators.prohibited_domains])),
                ('phone_number', models.CharField(blank=True, max_length=14, null=True, unique=True, validators=[django.core.validators.RegexValidator('\\d{10,14}')])),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('birthdate', models.DateField(blank=True, default=datetime.date.today, null=True, validators=[students.validators.older_than_18])),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatar')),
                ('resume', models.FileField(blank=True, null=True, upload_to='resume')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_course', to='courses.course')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
