# Generated by Django 3.2.8 on 2021-11-01 16:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('time', models.TimeField(default=django.utils.timezone.now)),
                ('length', models.CharField(choices=[('0.5', '1/2 Hour'), ('1.0', '1 Hour'), ('1.5', '1 1/2 Hour'), ('2.0', '2 Hour'), ('2.5', '2 1/2 Hour'), ('3.0', '3 Hour'), ('3.5', '3 1/2 Hour'), ('4.0', '4 Hour'), ('0.0', 'Other')], default='2.0', max_length=4)),
                ('type', models.CharField(choices=[('i', 'Internal Event'), ('c', 'Painting with a Purpose Event'), ('s', 'Stanrd Event'), ('p', 'Paint Pour Event'), ('t', 'Other Tax Free Event')], default='s', max_length=1)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]