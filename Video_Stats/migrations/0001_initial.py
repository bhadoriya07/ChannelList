# Generated by Django 3.2.5 on 2022-02-10 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='stats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videoLink', models.TextField(max_length=100)),
                ('brand', models.CharField(max_length=50)),
                ('brand_category', models.CharField(max_length=50)),
                ('cm_name', models.CharField(max_length=20)),
                ('cost', models.CharField(max_length=10)),
                ('live_date', models.CharField(max_length=10)),
                ('inf_name', models.CharField(max_length=20)),
                ('channel_link', models.TextField(max_length=100)),
                ('inf_category', models.CharField(max_length=10)),
                ('video_duration', models.CharField(max_length=10)),
                ('views_count', models.CharField(max_length=10)),
                ('cost_perviews', models.CharField(max_length=10)),
                ('comments', models.CharField(max_length=10)),
                ('video_title', models.TextField(max_length=200)),
            ],
        ),
    ]
