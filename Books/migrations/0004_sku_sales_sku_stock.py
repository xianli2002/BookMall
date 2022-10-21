# Generated by Django 4.0.5 on 2022-10-19 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0003_alter_bookscategory_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='sku',
            name='sales',
            field=models.IntegerField(default=0, verbose_name='销量'),
        ),
        migrations.AddField(
            model_name='sku',
            name='stock',
            field=models.IntegerField(default=0, verbose_name='库存'),
        ),
    ]