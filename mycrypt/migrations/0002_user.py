# Generated by Django 4.0.4 on 2022-07-26 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycrypt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=30)),
                ('passWord', models.CharField(max_length=50)),
                ('role', models.CharField(max_length=30)),
            ],
        ),
    ]
