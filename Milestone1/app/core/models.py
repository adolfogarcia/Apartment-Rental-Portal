from django.db import models
from django.shortcuts import reverse


class RoommateApplication(models.Model):
    # Genders
    MALE = 'M'
    FEMALE = 'F'
    ANY = 'A'

    # Years
    FRESHMAN = 'F'
    SOPHOMORE = 'S'
    JUNIOR = 'J'
    SENIOR = 'N'
    GRAD = 'G'

    # Cleanliness
    CLEAN = 'C'
    INTERMEDIATE = 'I'
    MESSY = 'M'

    # Yourself
    name = models.CharField(
        max_length=30,
    )
    gender = models.CharField(
        max_length=1,
        choices=(
            (MALE, 'Male'),
            (FEMALE, 'Female'),
        ),
    )
    year = models.CharField(
        max_length=1,
        choices=(
            (FRESHMAN, 'Freshman'),
            (SOPHOMORE, 'Sophomore'),
            (JUNIOR, 'Junior'),
            (SENIOR, 'Senior'),
            (GRAD, 'Grad Student'),
        )
    )
    cleanliness = models.CharField(
        max_length=1,
        choices=(
            (CLEAN, 'Clean'),
            (INTERMEDIATE, 'Intermediate'),
            (MESSY, 'Messy'),
        )
    )
    smoking = models.BooleanField()

    # Looking for
    looking_for_gender = models.CharField(
        max_length=1,
        choices=(
            (MALE, 'Male'),
            (FEMALE, 'Female'),
            (ANY, 'Any'),
        ),
    )
    price_floor = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    price_ceiling = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('roommate_detail', kwargs={'roommate_pk': self.pk})

    def find_compatible_roommates(self):
        # Exclude self!
        roommates = self.__class__.objects.exclude(pk=self.pk)

        # Filter good criteria
        roommates = roommates.filter(
            year=self.year,
            cleanliness=self.cleanliness,
            price_ceiling__gte=self.price_floor,
            price_floor__lte=self.price_ceiling,
            smoking=self.smoking,
        )

        # Filter looking for gender
        if self.looking_for_gender != self.ANY:
            roommates = roommates.filter(
                looking_for_gender=self.looking_for_gender,
            )

        return roommates

    def find_compatible_apartments(self):
        return Apartment.objects.filter(
            price__lte=self.price_ceiling,
            price__gte=self.price_floor,
        )


class Apartment(models.Model):
    name = models.CharField(max_length=20)

    num_rooms = models.IntegerField()
    num_bath = models.DecimalField(
        max_digits=3,
        decimal_places=1,
    )
    num_kitchen = models.IntegerField()

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    address = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('apartment_detail', kwargs={'apartment_pk': self.pk})

    def find_compatible_tenants(self):
        return RoommateApplication.objects.filter(
            price_ceiling__gte=self.price,
            price_floor__lte=self.price,
        )
