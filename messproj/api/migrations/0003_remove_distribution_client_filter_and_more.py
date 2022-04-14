# Generated by Django 4.0.3 on 2022-04-07 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_client_mobile_operator_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='distribution',
            name='client_filter',
        ),
        migrations.AlterField(
            model_name='distribution',
            name='finish_datetime',
            field=models.DateTimeField(null=True, verbose_name='дата и время окончания рассылки'),
        ),
    ]