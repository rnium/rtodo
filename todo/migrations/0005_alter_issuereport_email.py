# Generated by Django 3.2.9 on 2022-07-01 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_feedback_issuereport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuereport',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
