from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('B_authentication', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Education_group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now_add=True)),
                ('education_filial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='B_authentication.education_filial')),
                ('education_main', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='B_authentication.education_main')),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_subject', models.CharField(max_length=150)),
                ('price_subject', models.CharField(max_length=150)),
                ('education_filial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='B_authentication.education_filial')),
                ('teacher_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Education_students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_tg_id', models.CharField(max_length=50, null=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('midile_name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('phone_father', models.CharField(max_length=100)),
                ('phone_mother', models.CharField(max_length=100)),
                ('passort_seria', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('price', models.CharField(max_length=250)),
                ('payment_date', models.DateField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now_add=True)),
                ('education_filial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='B_authentication.education_filial')),
                ('education_main', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='B_authentication.education_main')),
                ('group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='C_crud.education_group')),
            ],
        ),
        migrations.AddField(
            model_name='education_group',
            name='subject_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='C_crud.subjects'),
        ),
    ]
