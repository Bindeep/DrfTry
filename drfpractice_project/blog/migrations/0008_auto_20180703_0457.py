# Generated by Django 2.0.6 on 2018-07-03 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_article_is_archived'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='created_time',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='updated_time',
            new_name='updated_at',
        ),
    ]
