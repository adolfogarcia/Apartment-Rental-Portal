from django import forms
from . import models


class RoommateForm(forms.ModelForm):
    class Meta:
        model = models.RoommateApplication
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        price_floor = cleaned_data.get["price_floor"]
        price_ceiling = cleaned_data.get["price_ceiling"]

        if price_floor > price_ceiling:
            self.add_error(
                "price_floor",
                "Price floor cannot be greater than price ceiling"
            )


class ApartmentForm(forms.ModelForm):
    class Meta:
        model = models.Apartment
        fields = '__all__'
