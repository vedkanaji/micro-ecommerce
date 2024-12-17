from django.db import models
from django.conf import settings
# Create your models here.

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, blank=True)
    stripe_price = models.IntegerField(default=0)
    completed = models.BooleanField(default=False) 
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.quantity} of {self.product.name} by {self.user.username}'