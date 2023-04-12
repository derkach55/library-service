# Generated by Django 4.1.6 on 2023-04-11 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrowing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowing',
            name='actual_return',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='borrowing',
            name='borrow_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='borrowing',
            name='expected_return',
            field=models.DateTimeField(),
        ),
    ]
