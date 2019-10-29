from django.test import TestCase


class TestRoommateModel(TestCase):
    def test_find_compatible_roommates(self):
        pass

    def test_find_compatible_apartments(self):
        pass


class TestApartmentModel(TestCase):
    def test_find_compatible_tenants(self):
        pass


class TestViews(TestCase):
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
        pass

    # Does not need to be tested! Has no special functionality
    # def test_apartment_form(pass):
    #     pass

    def test_apartment_list(self):
        pass

    def test_apartment_detail(self):
        pass
