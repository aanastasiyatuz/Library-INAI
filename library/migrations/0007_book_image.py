# Generated by Django 3.2.8 on 2021-10-14 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(default=1, upload_to='books'),
            preserve_default=False,
        ),
    ]
