# Generated by Django 5.2.1 on 2025-07-06 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oms', '0002_alter_order_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at']},
        ),
        migrations.RemoveField(
            model_name='order',
            name='date',
        ),
    ]
