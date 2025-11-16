# forms.py

from django import forms

USER_TYPE_CHOICES = (
    ('customer', 'Customer'),
    ('vendor', 'Vendor/Seller'),
    ('admin', 'Administrator'),
)

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput) 
    
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Account Type"
    )
    
    phone = forms.CharField(max_length=20, required=False)
    location = forms.CharField(max_length=100, required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(
                "Password and Confirm Password fields do not match."
            )
        return cleaned_data