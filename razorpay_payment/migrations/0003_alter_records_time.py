# Generated by Django 3.2.3 on 2021-06-02 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('razorpay_payment', '0002_auto_20210602_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='records',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
