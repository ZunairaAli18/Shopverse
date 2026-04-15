from django import forms
from .models import Store


class StoreForm(forms.ModelForm):
    class Meta:
        model  = Store
        fields = ['name', 'description', 'logo', 'banner']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'