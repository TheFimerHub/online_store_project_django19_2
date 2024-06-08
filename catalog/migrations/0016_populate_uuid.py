from django.db import migrations, models
import uuid

def generate_uuids(apps, schema_editor):
    Version = apps.get_model('catalog', 'Version')
    for version in Version.objects.all():
        version.uuid = uuid.uuid4()
        version.save()

class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_alter_product_options_alter_version_options_and_more'),
    ]

    operations = [
        migrations.RunPython(generate_uuids),
    ]

