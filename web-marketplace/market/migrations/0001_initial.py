# Generated by Django 5.0.3 on 2024-03-06 17:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Broadcast',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('picture_path', models.CharField(max_length=255)),
                ('telegram_has', models.BooleanField()),
                ('web_has', models.BooleanField(default=False)),
                ('sent_at', models.DateTimeField(default=False)),
            ],
            options={
                'db_table': 'broadcasts',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BroadcastSent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('broadcast_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'broadcasts_sent',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CartItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_cart_id', models.IntegerField()),
                ('product_id', models.IntegerField()),
                ('amount', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Cart Item',
                'verbose_name_plural': 'Cart Items',
                'db_table': 'cart_items',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': 'categories',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
            ],
            options={
                'verbose_name': 'FAQ',
                'verbose_name_plural': 'FAQs',
                'db_table': 'faq',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('picture_path', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.BigIntegerField()),
                ('telegram_has', models.BooleanField(default=False)),
                ('web_has', models.BooleanField(default=False)),
                ('discount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_visible', models.BooleanField(default=True)),
                ('article', models.CharField(default=None, max_length=36, unique=True)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'db_table': 'products',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Subcategory',
                'verbose_name_plural': 'Subcategories',
                'db_table': 'subcategories',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('cart_hash', models.CharField(default=None, max_length=36, unique=True)),
                ('is_bought', models.BooleanField()),
            ],
            options={
                'verbose_name': 'User Cart',
                'verbose_name_plural': 'User Carts',
                'db_table': 'user_cart',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('chat_id', models.CharField(max_length=255)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('role', models.CharField(choices=[('user', 'User'), ('manager', 'Manager'), ('admin', 'Admin'), ('superadmin', 'Superadmin')], default='user', max_length=255)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='YooInvoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('service_id', models.CharField(max_length=255, null=True)),
                ('cart_id', models.IntegerField(null=True)),
                ('status', models.CharField(max_length=255, null=True)),
                ('value', models.CharField(max_length=255, null=True)),
                ('currency', models.CharField(max_length=255, null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('paid', models.BooleanField(default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'YooInvoice',
                'verbose_name_plural': 'YooInvoices',
                'db_table': 'yoo_invoices',
                'managed': False,
            },
        ),
    ]