from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localization', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='language',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='language',
            name='updated_at',
        ),
    ]
