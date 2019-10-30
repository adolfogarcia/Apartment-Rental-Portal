from django.test import TestCase
from core.models import RoommateApplication
from django.shortcuts import reverse


class TestRoommateModel(TestCase):
    def test_find_compatible_roommates(self):
        pass

    def test_find_compatible_apartments(self):
        pass


class TestApartmentModel(TestCase):
    def test_find_compatible_tenants(self):
        pass


class TestViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.roommate = RoommateApplication.objects.create(
            name="Adolfo",
            gender=RoommateApplication.MALE,
            looking_for_gender=RoommateApplication.MALE,
            year=RoommateApplication.SENIOR,
            cleanliness=RoommateApplication.CLEAN,
            smoking=True,
            price_ceiling=1000,
            price_floor=500,
        )

        cls.compat_roommate = RoommateApplication.objects.create(
            name="Andrew",
            gender=RoommateApplication.MALE,
            looking_for_gender=RoommateApplication.MALE,
            year=RoommateApplication.SENIOR,
            cleanliness=RoommateApplication.CLEAN,
            smoking=True,
            price_ceiling=1000,
            price_floor=500,
        )

        cls.incompat_roommate = RoommateApplication.objects.create(
            name="El Stinko",
            gender=RoommateApplication.FEMALE,
            looking_for_gender=RoommateApplication.FEMALE,
            year=RoommateApplication.FRESHMAN,
            cleanliness=RoommateApplication.MESSY,
            smoking=False,
            price_ceiling=1500,
            price_floor=1100,
        )

    def test_home(self):
        pass

    def test_tenant_home(self):
        pass

    def test_landlord_home(self):
        pass

    def test_roommate_form(self):
        pass

    def test_roommate_list(self):
        pass

    def test_good_roommate_list(self):
        pass

    def test_roommate_detail(self):
        response = self.client.get(reverse('roommate_detail', kwargs={'roommate_pk': self.roommate.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertInHTML('Adolfo', response.content)

    # Does not need to be tested! Has no special functionality
    # def test_apartment_form(pass):
    #     pass

    def test_apartment_list(self):
        pass

    def test_apartment_detail(self):
        pass
