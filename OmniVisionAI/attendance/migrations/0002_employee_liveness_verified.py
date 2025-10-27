# Generated manually for liveness_verified field addition

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='liveness_verified',
            field=models.BooleanField(default=False, help_text='Whether liveness detection was completed during registration'),
        ),
    ]
