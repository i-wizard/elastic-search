from math import radians, cos, sin, asin, sqrt

from django.db import models

from helpers.db_helpers import BaseAbstractModel


class Character(BaseAbstractModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    occupation = models.CharField(max_length=255)
    is_suspect = models.BooleanField(
        default=False, help_text="This field will be False by default because you are innocent until proven guilty.")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Location(BaseAbstractModel):
    # latitude integers are +90 to -90. 7 decimal places are sufficient to store coordinates with centimeter [cm] accuracy
    latitude = models.DecimalField(max_digits=9, decimal_places=7)
    # longitude integers are +180 to -180. 7 decimal places are sufficient to store coordinates with centimeter [cm] accuracy
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
