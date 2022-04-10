# Generated by Django 3.2.8 on 2022-04-09 15:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TypicalSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('monday_8am', models.BooleanField(default=True)),
                ('monday_9am', models.BooleanField(default=True)),
                ('monday_10am', models.BooleanField(default=True)),
                ('monday_11am', models.BooleanField(default=True)),
                ('monday_12pm', models.BooleanField(default=True)),
                ('monday_1pm', models.BooleanField(default=True)),
                ('monday_2pm', models.BooleanField(default=True)),
                ('monday_3pm', models.BooleanField(default=True)),
                ('monday_4pm', models.BooleanField(default=True)),
                ('monday_5pm', models.BooleanField(default=True)),
                ('monday_6pm', models.BooleanField(default=True)),
                ('monday_7pm', models.BooleanField(default=True)),
                ('monday_8pm', models.BooleanField(default=True)),
                ('monday_9pm', models.BooleanField(default=True)),
                ('monday_10pm', models.BooleanField(default=True)),
                ('monday_recurrence', models.CharField(choices=[('w', 'Every Week'), ('b', 'Every Other Week'), ('m', 'Once a Month'), ('a', 'Open from Time To Time - Just Ask Me')], default='w', max_length=1)),
                ('tuesday_8am', models.BooleanField(default=True)),
                ('tuesday_9am', models.BooleanField(default=True)),
                ('tuesday_10am', models.BooleanField(default=True)),
                ('tuesday_11am', models.BooleanField(default=True)),
                ('tuesday_12pm', models.BooleanField(default=True)),
                ('tuesday_1pm', models.BooleanField(default=True)),
                ('tuesday_2pm', models.BooleanField(default=True)),
                ('tuesday_3pm', models.BooleanField(default=True)),
                ('tuesday_4pm', models.BooleanField(default=True)),
                ('tuesday_5pm', models.BooleanField(default=True)),
                ('tuesday_6pm', models.BooleanField(default=True)),
                ('tuesday_7pm', models.BooleanField(default=True)),
                ('tuesday_8pm', models.BooleanField(default=True)),
                ('tuesday_9pm', models.BooleanField(default=True)),
                ('tuesday_10pm', models.BooleanField(default=True)),
                ('tuesday_recurrence', models.CharField(choices=[('w', 'Every Week'), ('b', 'Every Other Week'), ('m', 'Once a Month'), ('a', 'Open from Time To Time - Just Ask Me')], default='w', max_length=1)),
                ('wednesday_8am', models.BooleanField(default=True)),
                ('wednesday_9am', models.BooleanField(default=True)),
                ('wednesday_10am', models.BooleanField(default=True)),
                ('wednesday_11am', models.BooleanField(default=True)),
                ('wednesday_12pm', models.BooleanField(default=True)),
                ('wednesday_1pm', models.BooleanField(default=True)),
                ('wednesday_2pm', models.BooleanField(default=True)),
                ('wednesday_3pm', models.BooleanField(default=True)),
                ('wednesday_4pm', models.BooleanField(default=True)),
                ('wednesday_5pm', models.BooleanField(default=True)),
                ('wednesday_6pm', models.BooleanField(default=True)),
                ('wednesday_7pm', models.BooleanField(default=True)),
                ('wednesday_8pm', models.BooleanField(default=True)),
                ('wednesday_9pm', models.BooleanField(default=True)),
                ('wednesday_10pm', models.BooleanField(default=True)),
                ('wednesday_recurrence', models.CharField(choices=[('w', 'Every Week'), ('b', 'Every Other Week'), ('m', 'Once a Month'), ('a', 'Open from Time To Time - Just Ask Me')], default='w', max_length=1)),
                ('thursday_8am', models.BooleanField(default=True)),
                ('thursday_9am', models.BooleanField(default=True)),
                ('thursday_10am', models.BooleanField(default=True)),
                ('thursday_11am', models.BooleanField(default=True)),
                ('thursday_12pm', models.BooleanField(default=True)),
                ('thursday_1pm', models.BooleanField(default=True)),
                ('thursday_2pm', models.BooleanField(default=True)),
                ('thursday_3pm', models.BooleanField(default=True)),
                ('thursday_4pm', models.BooleanField(default=True)),
                ('thursday_5pm', models.BooleanField(default=True)),
                ('thursday_6pm', models.BooleanField(default=True)),
                ('thursday_7pm', models.BooleanField(default=True)),
                ('thursday_8pm', models.BooleanField(default=True)),
                ('thursday_9pm', models.BooleanField(default=True)),
                ('thursday_10pm', models.BooleanField(default=True)),
                ('thursday_recurrence', models.CharField(choices=[('w', 'Every Week'), ('b', 'Every Other Week'), ('m', 'Once a Month'), ('a', 'Open from Time To Time - Just Ask Me')], default='w', max_length=1)),
                ('friday_8am', models.BooleanField(default=True)),
                ('friday_9am', models.BooleanField(default=True)),
                ('friday_10am', models.BooleanField(default=True)),
                ('friday_11am', models.BooleanField(default=True)),
                ('friday_12pm', models.BooleanField(default=True)),
                ('friday_1pm', models.BooleanField(default=True)),
                ('friday_2pm', models.BooleanField(default=True)),
                ('friday_3pm', models.BooleanField(default=True)),
                ('friday_4pm', models.BooleanField(default=True)),
                ('friday_5pm', models.BooleanField(default=True)),
                ('friday_6pm', models.BooleanField(default=True)),
                ('friday_7pm', models.BooleanField(default=True)),
                ('friday_8pm', models.BooleanField(default=True)),
                ('friday_9pm', models.BooleanField(default=True)),
                ('friday_10pm', models.BooleanField(default=True)),
                ('friday_recurrence', models.CharField(choices=[('w', 'Every Week'), ('b', 'Every Other Week'), ('m', 'Once a Month'), ('a', 'Open from Time To Time - Just Ask Me')], default='w', max_length=1)),
                ('saturday_8am', models.BooleanField(default=True)),
                ('saturday_9am', models.BooleanField(default=True)),
                ('saturday_10am', models.BooleanField(default=True)),
                ('saturday_11am', models.BooleanField(default=True)),
                ('saturday_12pm', models.BooleanField(default=True)),
                ('saturday_1pm', models.BooleanField(default=True)),
                ('saturday_2pm', models.BooleanField(default=True)),
                ('saturday_3pm', models.BooleanField(default=True)),
                ('saturday_4pm', models.BooleanField(default=True)),
                ('saturday_5pm', models.BooleanField(default=True)),
                ('saturday_6pm', models.BooleanField(default=True)),
                ('saturday_7pm', models.BooleanField(default=True)),
                ('saturday_8pm', models.BooleanField(default=True)),
                ('saturday_9pm', models.BooleanField(default=True)),
                ('saturday_10pm', models.BooleanField(default=True)),
                ('saturday_recurrence', models.CharField(choices=[('w', 'Every Week'), ('b', 'Every Other Week'), ('m', 'Once a Month'), ('a', 'Open from Time To Time - Just Ask Me')], default='w', max_length=1)),
                ('sunday_8am', models.BooleanField(default=True)),
                ('sunday_9am', models.BooleanField(default=True)),
                ('sunday_10am', models.BooleanField(default=True)),
                ('sunday_11am', models.BooleanField(default=True)),
                ('sunday_12pm', models.BooleanField(default=True)),
                ('sunday_1pm', models.BooleanField(default=True)),
                ('sunday_2pm', models.BooleanField(default=True)),
                ('sunday_3pm', models.BooleanField(default=True)),
                ('sunday_4pm', models.BooleanField(default=True)),
                ('sunday_5pm', models.BooleanField(default=True)),
                ('sunday_6pm', models.BooleanField(default=True)),
                ('sunday_7pm', models.BooleanField(default=True)),
                ('sunday_8pm', models.BooleanField(default=True)),
                ('sunday_9pm', models.BooleanField(default=True)),
                ('sunday_10pm', models.BooleanField(default=True)),
                ('sunday_recurrence', models.CharField(choices=[('w', 'Every Week'), ('b', 'Every Other Week'), ('m', 'Once a Month'), ('a', 'Open from Time To Time - Just Ask Me')], default='w', max_length=1)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schedule_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schedule_updated_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]