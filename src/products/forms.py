from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Product, ProductAttachment

<<<<<<< HEAD
input_css_class = "form-control"
=======
input_css_class = 'form-control'
>>>>>>> dev-branch


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'handle', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
<<<<<<< HEAD
        # self.fields['name'].widget.attrs['placeholder'] = "Your name"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class
=======
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': input_css_class})
>>>>>>> dev-branch


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
<<<<<<< HEAD
        fields = ["image", 'name', 'handle', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['placeholder'] = "Your name"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class


=======
        fields = ['name', 'handle', 'price', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': input_css_class})
>>>>>>> dev-branch

class ProductAttachmentForm(forms.ModelForm):
    class Meta:
        model = ProductAttachment
<<<<<<< HEAD
        fields = ["file", 'name', 'is_free', 'active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['placeholder'] = "Your name"
        for field in self.fields:
            if field in ['is_free', 'active']:
                continue
            self.fields[field].widget.attrs['class'] = input_css_class


ProductAttachmentModelFormSet = modelformset_factory(
    ProductAttachment,
    form=ProductAttachmentForm,
    fields = ['file', 'name','is_free', 'active'],
    extra=0,
    can_delete=True
)

ProductAttachmentInlineFormSet = inlineformset_factory(
    Product,
    ProductAttachment,
    form = ProductAttachmentForm,
    formset = ProductAttachmentModelFormSet,
    fields = ['file', 'name','is_free', 'active'],
    extra=0,
    can_delete=True
)
=======
        fields = ['file', 'name', 'is_free', 'active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field in ['is_free', 'active']:
                continue
            self.fields[field].widget.attrs.update({'class': input_css_class})

ProductAttachmentModelFormSet = modelformset_factory(
    ProductAttachment,
    fields=['file', 'name', 'is_free', 'active'],
    extra=0,
    can_delete=False
)

ProductAttachmentInLineFormSet = inlineformset_factory(
    Product,
    ProductAttachment,
    formset=ProductAttachmentModelFormSet,
    fields=['file', 'name', 'is_free', 'active'],
    extra=0,
    can_delete=False
)
>>>>>>> dev-branch
