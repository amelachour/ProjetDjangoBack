# Generated by Django 5.1.1 on 2024-10-30 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_alter_userprofile_teaching_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='teaching_subject',
            field=models.CharField(blank=True, default='unknown', max_length=100, null=True),
        ),
    ]
