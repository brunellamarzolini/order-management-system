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
