# Generated by Django 5.1.1 on 2024-10-07 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=50)),
                ('catagory', models.CharField(max_length=40)),
                ('price', models.FloatField()),
                ('transpotation', models.CharField(max_length=50)),
                ('guide', models.CharField(max_length=50)),
                ('details', models.CharField(max_length=100)),
            ],
        ),
    ]
