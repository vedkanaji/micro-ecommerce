<<<<<<< HEAD
# Generated by Django 4.1.7 on 2023-03-24 18:24
=======
# Generated by Django 4.1.13 on 2024-12-17 20:04
>>>>>>> dev-branch

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
<<<<<<< HEAD
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0004_productattachment_name'),
=======
        ('products', '0004_productattachment_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
>>>>>>> dev-branch
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
<<<<<<< HEAD
                ('completed', models.BooleanField(default=False)),
                ('stripe_price', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
=======
                ('stripe_price', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('quantity', models.PositiveIntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
>>>>>>> dev-branch
            ],
        ),
    ]