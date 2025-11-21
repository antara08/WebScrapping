from django.db import models
import uuid
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError



TYPES = ["red", "white", "rose", "specialty"]
SWEETNESS = ["dry", "off-dry", "sweet", "very-sweet"]

TYPE_CHOICES=[(t,t.replace("-"," ").capitalize()) for t in TYPES ]
SWEETNESS_CHOICES=[(s,s.replace("-"," ").capitalize()) for s in SWEETNESS ]

class Wine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    is_vintage = models.BooleanField(default=False)
    sweetness = models.CharField(max_length=20, choices=SWEETNESS_CHOICES)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    def clean(self):
        errors = {}

        # enforce max_length manually (because your form wasn't catching it)
        if self.name and len(self.name) > 200:
            errors["name"] = "Name cannot exceed 200 characters."

        if self.manufacturer and len(self.manufacturer) > 200:
            errors["manufacturer"] = "Manufacturer cannot exceed 200 characters."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()  # runs validations before saving
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.name} ({self.manufacturer})"
    

class Store(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)

    def clean(self):
        errors = {}

        # Enforce max_length manually so we catch it before DB-level exception
        if self.name and len(self.name) > 200:
            errors["name"] = "Name cannot exceed 200 characters."

        if self.address and len(self.address) > 300:
            errors["address"] = "Address cannot exceed 300 characters."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()  # runs clean() + field validations
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
    

class StoreWine(models.Model):
    id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='inventories')
    wine = models.ForeignKey(Wine, on_delete=models.CASCADE, related_name='inventories')
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['store', 'wine'],
                name='unique_store_wine',
            )
        ]

    def __str__(self):
        return f"{self.store} - {self.wine} ({self.quantity})"    