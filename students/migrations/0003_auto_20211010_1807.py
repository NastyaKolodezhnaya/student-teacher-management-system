# Generated by Django 3.2.7 on 2021-10-10 15:07

import datetime
import django.core.validators
from django.db import migrations, models
import students.validators


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_alter_student_birthdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='phone_number',
            field=models.CharField(max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='birthdate',
            field=models.DateField(default=datetime.date(2021, 10, 10), null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(max_length=120, null=True, validators=[students.validators.no_elon_validator]),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=60, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=80, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
    ]
