# Generated by Django 2.2.1 on 2019-06-12 01:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0005_auto_20190612_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='reply_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='reply', to=settings.AUTH_USER_MODEL),
        ),
    ]