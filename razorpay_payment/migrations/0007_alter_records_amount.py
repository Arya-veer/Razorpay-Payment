# Generated by Django 3.2.3 on 2021-06-03 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('razorpay_payment', '0006_alter_records_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='records',
            name='amount',
            field=models.PositiveIntegerField(),
        ),
    ]