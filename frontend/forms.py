from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address']  # Include only the fields that exist in the model
from django import forms
from .models import Product, Scheme

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_image', 'product_name', 'brand_name', 'product_price']  # Add other fields if necessary

class SchemeForm(forms.ModelForm):
    class Meta:
        model = Scheme
        fields = ['scheme_image', 'scheme_name', 'ministry', 'scheme_summary', 'scheme_link']  # Add other fields if necessary
