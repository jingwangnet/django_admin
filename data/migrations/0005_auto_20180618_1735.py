# Generated by Django 2.0.3 on 2018-06-18 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_auto_20180617_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='province',
            name='name',
            field=models.CharField(help_text='省份', max_length=5, unique=True),
        ),
    ]
