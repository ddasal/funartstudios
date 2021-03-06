# Generated by Django 3.2.8 on 2021-11-11 14:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0034_auto_20211110_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('type', models.CharField(choices=[('h', 'Twist at Home Kit(s)'), ('p', 'Pop In and Paint(s)'), ('r', 'Event Reservation(s)')], default='h', max_length=1)),
            ],
        ),
    ]
