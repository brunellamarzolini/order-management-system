# Generated by Django 5.2.1 on 2025-07-06 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oms', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-date']},
        ),
    ]
