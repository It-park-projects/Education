# Generated by Django 4.1.1 on 2022-09-14 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('C_crud', '0002_alter_education_students_create_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education_students',
            name='payment_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
