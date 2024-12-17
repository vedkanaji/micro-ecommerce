from django.contrib import admin
from .models import Product, ProductAttachment
from django import forms
from django.core.exceptions import ValidationError

# Custom Form for ProductAttachment to handle file validation
class ProductAttachmentForm(forms.ModelForm):
    class Meta:
        model = ProductAttachment
        fields = ['name', 'product', 'file', 'is_free', 'active']
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file and self.instance.pk:
            # If the instance exists but no file is provided, check for required file validation
            raise ValidationError("File is required for this attachment.")
        return file

# Admin configuration for ProductAttachment
class ProductAttachmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'product', 'file', 'is_free', 'active']
    search_fields = ['name', 'product__name']
    form = ProductAttachmentForm

    def save_model(self, request, obj, form, change):
        # You can add custom save logic here if needed, otherwise just use the default behavior
        super().save_model(request, obj, form, change)

admin.site.register(Product)
admin.site.register(ProductAttachment, ProductAttachmentAdmin)