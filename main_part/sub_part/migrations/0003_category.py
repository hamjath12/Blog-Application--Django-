# Generated by Django 5.1.7 on 2025-03-20 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub_part', '0002_post_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
