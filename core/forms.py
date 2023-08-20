from django import forms

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100, label='First Name')
    last_name = forms.CharField(max_length=100, label='Last Name')
    address = forms.CharField(widget=forms.Textarea, label='Address')
    zip_code = forms.CharField(max_length=12, label='ZIP / Postal Code')
    city = forms.CharField(max_length=50, label='City')
    country = forms.CharField(max_length=50, label='Country')
    phone = forms.CharField(max_length=20, label='Phone Number')
    email = forms.EmailField(label='Email Address')


class UpdateQuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, required=True)
    cart_item_id = forms.IntegerField(widget=forms.HiddenInput())


