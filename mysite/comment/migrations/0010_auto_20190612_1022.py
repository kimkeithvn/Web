# Generated by Django 2.2.1 on 2019-06-12 02:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0009_auto_20190612_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='child_reply', to='comment.Comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='root',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='all_reply', to='comment.Comment'),
        ),
    ]
