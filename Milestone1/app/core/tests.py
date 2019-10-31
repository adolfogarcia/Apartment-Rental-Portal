from django.test import TestCase
from core.models import RoommateApplication
from django.shortcuts import reverse

from django.contrib.sessions.middleware import SessionMiddleware


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
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'ApartFinder')
        self.assertContains(response, 'Tenant')
        self.assertContains(response, 'Landlord')

    def test_tenant_home(self):
        """Tenant_home -> roommate_form if not logged in (to create account),
        otherwise renders tenant_home"""
        tenant_home_url = reverse('tenant_home')
        response = self.client.get(tenant_home_url)

        # Should redirect to roommate_form
        self.assertTrue(reverse('roommate_form') in response.url)

        # Make the user into Adolfo
        session = self.client.session
        session['user'] = self.roommate.pk
        session.save()

        # Try again now that logged in
        response = self.client.get(tenant_home_url)
        self.assertTemplateUsed(response, 'tenant_home.html')
        self.assertContains(response, 'Welcome Adolfo')

    def test_landlord_home(self):
        """Landlord always redirects to apartment_form to list apartment"""
        response = self.client.get(reverse('landlord_home'))
        self.assertTrue(reverse('apartment_form') in response.url)

    def test_roommate_form(self):
        """Test that submitting the roommate form creates the roommate on the list"""
        roommate_form_url = reverse('roommate_form')

        # Make sure roommate has not already been created
        response = self.client.get(reverse('roommate_list'))
        self.assertNotContains(response, 'Testdudette')

        # Sets csrftoken
        _ = self.client.get(roommate_form_url)
        csrftoken = self.client.cookies['csrftoken']

        # Submit the form data to URL
        self.client.post(roommate_form_url, data={
            'csrfmiddlewaretoken': csrftoken,
            'name': 'Testdudette',
            'gender': 'F',
            'year': 'G',
            'cleanliness': 'I',
            'smoking': True,
            'looking_for_gender': 'A',
            'price_floor': 500,
            'price_ceiling': 1500,
        })

        # Now roommate should be created
        response = self.client.get(reverse('roommate_list'))
        self.assertContains(response, 'Testdudette')

    def test_roommate_list(self):
        pass

    def test_good_roommate_list(self):
        pass

    def test_roommate_detail(self):
        response = self.client.get(reverse('roommate_detail', kwargs={'roommate_pk': self.roommate.pk}))
        self.assertContains(response, 'Adolfo')

    # Does not need to be tested! Has no special functionality
    # def test_apartment_form(pass):
    #     pass

    def test_apartment_list(self):
        pass

    def test_apartment_detail(self):
        pass
