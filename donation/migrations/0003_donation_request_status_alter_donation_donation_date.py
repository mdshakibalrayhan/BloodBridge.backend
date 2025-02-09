# Generated by Django 5.0.6 on 2025-01-28 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0002_alter_donation_donated_blood_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='request_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='donation',
            name='donation_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
