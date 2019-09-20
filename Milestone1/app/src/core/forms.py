from django import forms
from . import models


class RoommateForm(forms.ModelForm):
    class Meta:
        model = models.RoommateApplication
        fields = '__all__'


class ApartmentForm(forms.ModelForm):
    class Meta:
        model = models.Apartment
        fields = '__all__'
