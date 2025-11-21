from decimal import Decimal
from django import forms
from .models import Wine, Store, StoreWine


class WineForm(forms.ModelForm):
    class Meta:
        model = Wine
        fields = ["name", "manufacturer", "type", "is_vintage", "sweetness", "price"]
        widgets = {
            "name": forms.TextInput(attrs={"maxlength": 200}),
            "manufacturer": forms.TextInput(attrs={"maxlength": 200}),
        }


    def clean_name(self):
        name = self.cleaned_data.get("name", "")
        if len(name) > 200:
            raise forms.ValidationError("Name cannot exceed 200 characters.")
        return name

    def clean_manufacturer(self):
        manufacturer = self.cleaned_data.get("manufacturer", "")
        if len(manufacturer) > 200:
            raise forms.ValidationError("Manufacturer cannot exceed 200 characters.")
        return manufacturer

    def clean(self):
        cleaned = super().clean()
        price = cleaned.get("price")
        is_vintage = cleaned.get("is_vintage")

        # Custom validation: if price > 30, must be vintage
        if price is not None and price > Decimal("30.00") and not is_vintage:
            self.add_error(
                "is_vintage", "Wines over $30.00 must be marked as vintage."
            )

        return cleaned

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ["name", "address"]
        widgets = {
            "name": forms.TextInput(attrs={"maxlength": 200}),
            "address": forms.TextInput(attrs={"maxlength": 300}),
        }


    def clean_name(self):
        name = self.cleaned_data.get("name", "")
        if len(name) > 200:
            raise forms.ValidationError("Name cannot exceed 200 characters.")
        return name

    def clean_address(self):
        address = self.cleaned_data.get("address", "")
        if len(address) > 300:
            raise forms.ValidationError("Address cannot exceed 300 characters.")
        return address
    
    
class InventoryForm(forms.Form):
    store = forms.ModelChoiceField(queryset=Store.objects.all())
    wine = forms.ModelChoiceField(queryset=Wine.objects.all())
    quantity = forms.IntegerField(min_value=0)

    def save(self):
        store = self.cleaned_data["store"]
        wine = self.cleaned_data["wine"]
        quantity = self.cleaned_data["quantity"]

        # Update if (store, wine) exists, otherwise create
        obj, created = StoreWine.objects.update_or_create(
            store=store,
            wine=wine,
            defaults={"quantity": quantity},
        )
        return obj
