# Generated by Django 4.1.6 on 2023-04-18 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('borrowing', '0004_alter_borrowing_actual_return_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PAID', 'Payment Paid'), ('PENDING', 'Payment Pending')], max_length=7)),
                ('type', models.CharField(choices=[('PAYMENT', 'Payment type'), ('FINE', 'Fine type')], max_length=7)),
                ('session_url', models.CharField(max_length=255)),
                ('session_id', models.CharField(max_length=255)),
                ('money_to_pay', models.DecimalField(decimal_places=10, max_digits=19)),
                ('borrowing', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='borrowing.borrowing')),
            ],
        ),
    ]
