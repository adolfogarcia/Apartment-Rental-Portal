from django.contrib import admin

from . import models


@admin.register(models.RoommateApplication)
class RoommateApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    pass

