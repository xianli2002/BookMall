# Generated by Django 4.0.5 on 2022-10-18 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookscategory',
            name='parent',
            field=models.IntegerField(verbose_name='父类别'),
        ),
    ]
