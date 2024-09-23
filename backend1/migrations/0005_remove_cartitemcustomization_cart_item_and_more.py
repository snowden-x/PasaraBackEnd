# Generated by Django 5.0.6 on 2024-09-21 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend1', '0004_menutype_remove_product_available_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitemcustomization',
            name='cart_item',
        ),
        migrations.RemoveField(
            model_name='cartitemcustomization',
            name='option',
        ),
        migrations.RemoveField(
            model_name='product',
            name='available_option_types',
        ),
        migrations.RemoveField(
            model_name='option',
            name='menu_type',
        ),
        migrations.RemoveField(
            model_name='productdefaultoption',
            name='option',
        ),
        migrations.RemoveField(
            model_name='productdefaultoption',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='available_options',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='product',
            name='default_options',
            field=models.JSONField(default=dict),
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
        migrations.DeleteModel(
            name='CartItemCustomization',
        ),
        migrations.DeleteModel(
            name='MenuType',
        ),
        migrations.DeleteModel(
            name='Option',
        ),
        migrations.DeleteModel(
            name='ProductDefaultOption',
        ),
    ]
