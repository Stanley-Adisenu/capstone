# Generated by Django 5.0.3 on 2024-07-08 13:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_alter_course_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.level'),
        ),
    ]
