# Generated by Django 4.0.5 on 2022-10-17 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Areas', '0001_initial'),
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='default_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_address', to='Areas.address', verbose_name='默认地址'),
        ),
    ]
