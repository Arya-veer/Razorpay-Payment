from razorpay_payment.models import Records
from django.contrib.auth.models import User
from django import forms

class Donation_Form(forms.ModelForm):

    class Meta:
        model=Records
        fields=['amount']
        