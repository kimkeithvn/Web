# Generated by Django 2.0.13 on 2019-03-23 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20190322_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='read_count',
            field=models.IntegerField(default=0),
        ),
    ]
