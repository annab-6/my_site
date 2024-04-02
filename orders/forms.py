from django import forms
import re


class CreateOrderForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your first name",
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your last name",
            }
        )
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your phone number",
            }
        )
    )
    requires_delivery = forms.ChoiceField(
        choices=[("0", "No"), ("1", "Yes")],
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    delivery_address = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your delivery address",
            }
        )
    )
    payment_on_get = forms.ChoiceField(
        choices=[("0", "Payment by card"), ("1", "Cash/card upon receipt")],
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def clean_phone_number(self):
        """Validate phone number."""
        data = self.cleaned_data['phone_number']

        if not data.isdigit():
            raise forms.ValidationError("The phone number must contain only numbers")

        pattern = re.compile(r'^\d{10}$')
        if not pattern.match(data):
            raise forms.ValidationError("Invalid number ")

        return data
