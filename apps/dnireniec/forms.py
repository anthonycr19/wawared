from django import forms
from django.forms import PasswordInput
from models import ServicioReniec


class ServiceReniecForm(forms.ModelForm):
    passservice = forms.CharField(widget=PasswordInput())

    class Meta:
        model = ServicioReniec
