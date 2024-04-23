from django import forms

CATEGORIES = (
    ('Old Peoples Home', 'Old Peoples Home'),
    ('Orphanage', 'Orphanage')
)

PAYMENT_METHOD_CHOICES = (
    ('Paypal', 'Paypal'),
    ('Credit Card', 'Credit Card'),
    ('Bank Transfer', 'Bank Transfer'),
    ('Ecocash', 'Ecocash')
)

CURRENCIES = [
    ('USD', 'USD'),
    ('ZiG', 'ZiG'),
    ('ZAR', 'ZAR'),
]


class BeneficiaryRegistrationForm(forms.Form):
    category = forms.CharField(max_length=55, widget=forms.Select(attrs={'class': 'form-control'}, choices=CATEGORIES))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    name = forms.CharField(max_length=80, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cell = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=800, widget=forms.TextInput(attrs={'class': 'form-control'}))
    about = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    city = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    logo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    cover_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    latitude = forms.DecimalField(decimal_places=5, max_digits=10, required=False,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))
    longitude = forms.DecimalField(decimal_places=5, max_digits=10, required=False,
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))


class OnlineDonationForm(forms.Form):
    amount = forms.DecimalField(decimal_places=2, max_digits=50,
                                widget=forms.NumberInput(attrs={'class': 'form-control'}))
    currency = forms.CharField(max_length=55, widget=forms.Select(attrs={'class': 'form-control'}, choices=CURRENCIES))
    payment_method = forms.CharField(max_length=55, widget=forms.Select(attrs={'class': 'form-control'},
                                                                        choices=PAYMENT_METHOD_CHOICES))
    donor_name = forms.CharField(required=False, max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
    donor_email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    donor_cell = forms.CharField(required=False, max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
