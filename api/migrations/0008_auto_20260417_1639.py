from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_inventoryitem_itemgroup_itemunit_kompracustomer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(upload_to='profile_pics/', null=True, blank=True),
        ),
    ]