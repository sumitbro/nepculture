from django import forms
from django_countries.fields import CountryField
from .models import Shipping




Payment_choice=(
    ('E', 'eSewa'),
    ('K', 'Khalti')
)
class ShippingForm(forms.ModelForm):
    class Meta:
        model= Shipping
        fields= '__all__'
        exclude = ['user', 'item', 'order']

    # address1= forms.CharField()
    # address2= forms.CharField(required=False)
    # country= CountryField(blank_label='(select country)').formfield()
    # Zip= forms.CharField()
    # payment= forms.ChoiceField(widget=forms.RadioSelect, choices= Payment_choice)

