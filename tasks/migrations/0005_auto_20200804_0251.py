# Generated by Django 2.2.5 on 2020-08-04 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20200804_0241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prioritycounter',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]