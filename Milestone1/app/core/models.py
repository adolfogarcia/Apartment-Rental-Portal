from django.db import models


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
    looking_for_gender = models.BooleanField(
        null=True,
    )
    price_floor = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    price_ceiling = models.DecimalField(
        max_digits=12,
        decimal_places=2,
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
