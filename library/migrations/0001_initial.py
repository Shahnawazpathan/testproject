# Generated by Django 3.0.5 on 2023-09-02 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('isbn', models.CharField(max_length=13)),
                ('publisher', models.CharField(max_length=100)),
                ('page_count', models.IntegerField()),
                ('stock', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateField(null=True)),
                ('return_date', models.DateField(blank=True, null=True)),
                ('fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Book')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Member')),
            ],
        ),
    ]
