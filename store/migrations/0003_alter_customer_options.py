# Generated by Django 4.2.4 on 2023-08-13 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_orderdetail_orderid_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['-id']},
        ),
    ]
