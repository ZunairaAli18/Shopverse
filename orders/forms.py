from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    PAYMENT_CHOICES = (
        ('cod',    '💵 Cash on Delivery'),
        ('stripe', '💳 Pay with Card (Stripe)'),
    )

    payment_method = forms.ChoiceField(
        choices  = PAYMENT_CHOICES,
        widget   = forms.RadioSelect(),
        initial  = 'cod',
    )

    class Meta:
        model  = Order
        fields = ['full_name', 'phone', 'address', 'city']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'payment_method':
                field.widget.attrs['class'] = 'form-control'

        self.fields['full_name'].widget.attrs['placeholder'] = 'Enter your full name'
        self.fields['phone'].widget.attrs['placeholder']     = '0300-1234567'
        self.fields['address'].widget.attrs['placeholder']   = 'Street address, area'
        self.fields['city'].widget.attrs['placeholder']      = 'e.g. Karachi'