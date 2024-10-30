# Generated by Django 5.1.1 on 2024-10-30 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_userprofile_phone'),
    ]

    operations = [
        
        migrations.AddField(
            model_name='userprofile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='teaching_subject',
             field=models.CharField(max_length=100, null=False, default='Default Subject'), 
        ),
    ]
