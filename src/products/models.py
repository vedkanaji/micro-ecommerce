<<<<<<< HEAD
import pathlib
import stripe


from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from cfehome.storages.backends import ProtectedFileStorage
from cfehome.env import config

STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default=None)
stripe.api_key = STRIPE_SECRET_KEY


PROTECTED_MEDIA_ROOT = settings.PROTECTED_MEDIA_ROOT
protected_storage = (
    ProtectedFileStorage()
)  # FileSystemStorage(location=str(PROTECTED_MEDIA_ROOT))


# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE
    )
    stripe_product_id = models.CharField(max_length=220, blank=True, null=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    name = models.CharField(max_length=120)
    handle = models.SlugField(unique=True)  # slug
    price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    og_price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    stripe_price_id = models.CharField(max_length=220, blank=True, null=True)
    stripe_price = models.IntegerField(default=999)  # 100 * price
    price_changed_timestamp = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def display_name(self):
        return self.name

=======
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone
from pathlib import Path
from django.urls import reverse

# Create your models here.
PROTECTED_MEDIA_ROOT = settings.PROTECTED_MEDIA_ROOT
protected_storage = FileSystemStorage(location=str(PROTECTED_MEDIA_ROOT))


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    handle = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=3, default=999)
    og_price = models.DecimalField(max_digits=10, decimal_places=3, default=999)
    stripe_price = models.IntegerField(default=999)
    # stripe_price_id =
    price_changed_timestamp = models.DateTimeField(auto_now_add=False,
                                                   auto_now=False,
                                                   blank=True,
                                                   null=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.price != self.og_price:
            # price is changed
            self.og_price = self.price
            # trigger an api request for price changes
            self.stripe_price = int(self.price * 100)
            self.price_changed_timestamp = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'handle': self.handle})

    def get_manage_url(self):
        return reverse('products:manage', kwargs={'handle': self.handle})

>>>>>>> dev-branch
    @property
    def display_price(self):
        return self.price

<<<<<<< HEAD
    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        if self.name:
            stripe_product_r = stripe.Product.create(name=self.name)
            self.stripe_product_id = stripe_product_r.id
        if not self.stripe_price_id:
            stripe_price_obj = stripe.Price.create(
                product=self.stripe_product_id,
                unit_amount=self.stripe_price,
                currency="usd",
            )
            self.stripe_price_id = stripe_price_obj.id
        if self.price != self.og_price:
            # price changed
            self.og_price = self.price
            # trigger an API request for the price
            self.stripe_price = int(self.price * 100)
            if self.stripe_product_id:
                stripe_price_obj = stripe.Price.create(
                    product=self.stripe_product_id,
                    unit_amount=self.stripe_price,
                    currency="usd",
                )
                self.stripe_price_id = stripe_price_obj.id
            self.price_changed_timestamp = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"handle": self.handle})

    def get_manage_url(self):
        return reverse("products:manage", kwargs={"handle": self.handle})


def handle_product_attachment_upload(instance, filename):
    return f"products/{instance.product.handle}/attachments/{filename}"


class ProductAttachment(models.Model):
=======

def handle_product_attachment_upload(instance, filename):
    if not instance.product.handle:
        raise ValueError(f"Product {instance.product.id} does not have a valid handle.")
    return f'products/{instance.product.handle}/attachment/{filename}'


class ProductAttachment(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
>>>>>>> dev-branch
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=handle_product_attachment_upload, storage=protected_storage
    )
<<<<<<< HEAD
    name = models.CharField(max_length=120, null=True, blank=True)
=======
>>>>>>> dev-branch
    is_free = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

<<<<<<< HEAD
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = pathlib.Path(self.file.name).name  # stem, suffix
=======
    def __str__(self):
        return self.file.url

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = Path(self.file.name).name
>>>>>>> dev-branch
        super().save(*args, **kwargs)

    @property
    def display_name(self):
<<<<<<< HEAD
        return self.name or pathlib.Path(self.file.name).name

    def get_download_url(self):
        url_kwargs = {
            "handle": self.product.handle,
            "pk": self.pk,
        }
        return reverse("products:download", kwargs=url_kwargs)
=======
        return self.name or Path(self.file.name).name

    def get_download_url(self):
        return reverse('products:download', kwargs={'pk': self.pk,
                                                    'handle': self.product.handle})
>>>>>>> dev-branch
