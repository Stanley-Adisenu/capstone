# Generated by Django 5.0.3 on 2024-05-30 01:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_rename_name_topic_topic_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='topic_name',
            new_name='name',
        ),
    ]
