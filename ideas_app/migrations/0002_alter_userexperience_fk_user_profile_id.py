# Generated by Django 4.2.2 on 2023-08-31 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ideas_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userexperience',
            name='fk_user_profile_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_exp', to='ideas_app.userprofile'),
        ),
    ]
