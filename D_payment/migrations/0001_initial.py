# Generated by Django 4.1.1 on 2022-09-14 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('C_crud', '0002_alter_education_students_create_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_payment', models.CharField(blank=True, max_length=250)),
                ('payment_date', models.DateField(blank=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('full_student_name', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='C_crud.education_students')),
            ],
        ),
    ]
