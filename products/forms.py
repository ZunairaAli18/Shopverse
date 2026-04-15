from django import forms
from .models import Product, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = ['name', 'slug', 'category', 'description',
                  'price', 'stock', 'image', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'slug': forms.TextInput(attrs={'placeholder': 'auto-fill or type manually'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to every field
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ProductImageForm(forms.ModelForm):
    class Meta:
        model  = ProductImage
        fields = ['image', 'alt']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'