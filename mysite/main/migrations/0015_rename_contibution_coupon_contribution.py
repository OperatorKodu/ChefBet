# Generated by Django 3.2.4 on 2021-06-28 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_coupon_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='contibution',
            new_name='contribution',
        ),
    ]