# Generated by Django 5.1.4 on 2024-12-12 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microservices_hotelpayment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_id',
            field=models.CharField(max_length=24, primary_key=True, serialize=False),
        ),
    ]
