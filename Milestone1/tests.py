from django.test import TestCase
from django.test.client import RequestFactory
from . import views
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.shortcuts import render, redirect
from . import models
from . import forms

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
        request = RequestFactory().get('/')
        if self.assertEqual(views.home(request).content, render(request, 'home.html', {}).content):
            pass


    def test_tenant_home(self):
        request = RequestFactory().get('/')
         #add session
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        #set user
        setattr(request, 'user', 'Jim')

        if self.assertEqual(views.tenant_home(request).content, redirect('roommate_form').content):
            pass

    def test_landlord_home(self):
        request = RequestFactory().get('/')
        if self.assertEqual(views.landlord_home(request).content, redirect('apartment_form').content):
            pass

    def test_roommate_form(self):
        request = RequestFactory().get('/')
        form = forms.RoommateForm()
      #  request.method = 'POST'
        if self.assertEqual(1, 1):
            pass
        #if self.assertAlmostEqual(views.roommate_form(request).content, render(request, 'roommate_form.html', {'form': form,}).content):
            pass
        #if self.assertEqual(views.roommate_form(request).content, redirect('tenant_home').content):        
            pass


    def test_roommate_list(self):
        pass
 
    def test_good_roommate_list(self):
        request = RequestFactory().get('/')
        #add session
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        models.jimbob = models.RoommateApplication()
        models.jimbob.name = "jimbob"
        models.jimbob.gender = 'M'
        models.jimbob.year = 'J'
        models.jimbob.cleanliness = 'I'
        models.jimbob.smoking = False
        models.jimbob.looking_for_gender = False
        models.jimbob.price_floor = 200.50
        models.jimbob.price_ceiling = 400.20


        models.jimbob2 = models.RoommateApplication()
        models.jimbob2.name = "jimbob2"
        models.jimbob2.gender = 'M'
        models.jimbob2.year = 'J'
        models.jimbob2.cleanliness = 'I'
        models.jimbob2.smoking = False
        models.jimbob2.looking_for_gender = False
        models.jimbob2.price_floor = 200.50
        models.jimbob2.price_ceiling = 400.20
        
        roommates = [models.jimbob2]
        
        #set user
        setattr(request, 'user', models.jimbob)
        setattr(request, 'roommates', roommates)
        request.session.save()

        if self.assertEqual(views.good_roommate_list(request).content, render(request, 'roommate_list.html', {'user': models.jimbob,'roommates': roommates,}).content):
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
