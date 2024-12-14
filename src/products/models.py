from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone
# Create your models here.
PROTECTED_MEDIA_ROOT = settings.PROTECTED_MEDIA_ROOT
protected_storage = FileSystemStorage(location=str(PROTECTED_MEDIA_ROOT))

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    handle = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=3 , default=999)
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
            #price is changed
            self.og_price = self.price
            # trigger an api request for price changes
            self.stripe_price = int(self.price * 100)
            self.price_changed_timestamp = timezone.now()
            
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/products/{self.handle}/'
    
def handle_product_attachment_upload(instance, filename):
    return f'products/{instance.product.handle}/attachment/{filename}'

class ProductAttachment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.FileField(upload_to=handle_product_attachment_upload, storage=protected_storage)
    is_free = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.file.url