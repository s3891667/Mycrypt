# Generated by Django 3.2.12 on 2022-10-02 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('symbol', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('date', models.DateField()),
                ('author', models.CharField(max_length=30)),
                ('source', models.URLField()),
                ('status', models.CharField(choices=[('d', 'Draft'), ('p', 'Published'), ('w', 'Withdrawn')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('userName', models.CharField(max_length=30)),
                ('passWord', models.CharField(max_length=50)),
                ('role', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('coin', models.ManyToManyField(to='mycrypt.Coin')),
            ],
        ),
    ]
