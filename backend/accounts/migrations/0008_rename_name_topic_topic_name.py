# Generated by Django 5.0.3 on 2024-05-29 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_topic_room_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='name',
            new_name='topic_name',
        ),
    ]