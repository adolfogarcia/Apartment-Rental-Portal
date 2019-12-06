from django.test import TestCase
from core.models import RoommateApplication, Apartment
from core.forms import RoommateForm

from django.shortcuts import reverse


class ApartmentTestCase(TestCase):
    def login(self, roommate):
        session = self.client.session
        session['user'] = roommate.pk
        session.save()

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

        cls.compat_apartment = Apartment.objects.create(
            name='The House From Nightmare on Elm Street',
            num_rooms=1,
            num_bath=1,
            num_kitchen=1,
            price=750.00,
            address='123 Elm Street',  # Halloween themed
        )

        cls.incompat_apartment = Apartment.objects.create(
            name='The House of Usher',  # Halloween themed
            num_rooms=6,
            num_bath=6,
            num_kitchen=6,
            price=6666.66,
            address='123 Fake St.',
        )


class TestRoommateModel(ApartmentTestCase):
    def test_find_compatible_roommates(self):
        self.assertQuerysetEqual(
            self.roommate.find_compatible_roommates(),
            [repr(self.compat_roommate)],  # Doesn't include self or incompat
        )

    def test_find_compatible_apartments(self):
        self.assertQuerysetEqual(
            self.roommate.find_compatible_apartments(),
            [repr(self.compat_apartment)],  # Don't include incompat
        )


class TestRoommateForm(ApartmentTestCase):
    def test_validate(self):
        self.assertFalse(
            # Make sure custom validation script works
            RoommateForm(data={
                'name': "Fudgo",
                'gender': RoommateApplication.MALE,
                'looking_for_gender': RoommateApplication.MALE,
                'year': RoommateApplication.SENIOR,
                'cleanliness': RoommateApplication.CLEAN,
                'smoking': True,
                'price_ceiling': 500,  # Herein lies the error
                'price_floor': 1000,
            }).is_valid()
        )


class TestApartmentForm(ApartmentTestCase):
    def test_get(self):
        """Make sure the empty form can be created initially"""
        response = self.client.get(reverse('apartment_form'))

    def test_post_valid(self):
        """Make sure valid form creates object"""
        apartment_form_url = reverse('apartment_form')
        _ = self.client.get(apartment_form_url)

        csrftoken = self.client.cookies['csrftoken']

        self.client.post(apartment_form_url, data={
            'csrfmiddlewaretoken': csrftoken,
            'name': 'The White House',
            'num_rooms': 1,
            'num_bath': 1,
            'num_kitchen': 1,
            'price': 1000.00,
            'address': '1215 NE Myrtle St.',
        })

        apartment = Apartment.objects.order_by('id').last()

        # Object successfully created
        self.assertEqual(apartment.name, 'The White House')

    def test_post_invalid(self):
        """Make sure invalid form submission fails"""
        apartment_form_url = reverse('apartment_form')
        _ = self.client.get(apartment_form_url)

        csrftoken = self.client.cookies['csrftoken']

        response = self.client.post(apartment_form_url, follow=True, data={
            'csrfmiddlewaretoken': csrftoken,  # Token valid
            'name': 'Name that is way way too long this won\'t work',
            'num_rooms': 1,
            'num_bath': 1,
            'num_kitchen': 1,
            'price': 1000.00,
            'address': '1215 NE Myrtle St.',
        })

        # Failed, no redirect
        self.assertFalse(response.redirect_chain)


class TestApartmentModel(ApartmentTestCase):
    def test_find_compatible_tenants(self):
        self.assertQuerysetEqual(
            self.compat_apartment.find_compatible_tenants().order_by('name'),
            [repr(self.roommate), repr(self.compat_roommate)],
        )


class TestViews(ApartmentTestCase):
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
        self.login(self.roommate)

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

        # Submit the correct form data to URL
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
        """Make sure list is populated correctly"""
        roommate_list_url = reverse('roommate_list')

        response = self.client.get(roommate_list_url)

        # All users should be in the list
        self.assertContains(response, self.roommate.name)
        self.assertContains(response, self.compat_roommate.name)
        self.assertContains(response, self.incompat_roommate.name)

        # Login as Adolfo
        self.login(self.roommate)

        # Now Adolfo should be logged in
        response = self.client.get(roommate_list_url)
        self.assertContains(
            response,
            f"{self.roommate.name}, say hello to your new roommates"
        )

    def test_good_roommate_list(self):
        # Login as Adolfo
        self.login(self.roommate)

        response = self.client.get(reverse('good_roommate_list'))

        # Compatible roommate should be in last, incompat should not
        self.assertContains(response, self.compat_roommate.name)
        self.assertNotContains(response, self.incompat_roommate.name)

    def test_good_roommate_list_not_logged_in(self):
        with self.assertRaises(EnvironmentError):
            self.client.get(reverse('good_roommate_list'))

    def test_roommate_detail(self):
        roommate = self.roommate
        roommate_url = roommate.get_absolute_url()
        response = self.client.get(roommate_url)
        self.assertContains(response, roommate.name)
        self.assertTemplateUsed(response, 'roommate_detail.html')

    def test_apartment_list_not_logged_in(self):
        """Make sure all apartments are on list"""
        response = self.client.get(reverse('apartment_list'))

        self.assertContains(response, self.compat_apartment.name)
        self.assertContains(response, self.incompat_apartment.name)

    def test_apartment_list_logged_in(self):
        """Make sure all apartments are still on list"""
        self.login(self.compat_roommate)
        response = self.client.get(reverse('apartment_list'))

        self.assertContains(response, self.compat_roommate.name)
        self.assertContains(response, self.compat_apartment.name)
        self.assertContains(response, self.incompat_apartment.name)

    def test_apartment_detail(self):
        """Make sure apartment detail renders for an apartment"""
        apartment = self.compat_apartment
        url = apartment.get_absolute_url()
        response = self.client.get(url)
        self.assertContains(response, apartment.name)
        self.assertTemplateUsed(response, 'apartment_detail.html')
