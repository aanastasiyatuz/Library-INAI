# Generated by Django 3.2.8 on 2021-11-28 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_auto_20211015_0421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='library.book'),
        ),
    ]