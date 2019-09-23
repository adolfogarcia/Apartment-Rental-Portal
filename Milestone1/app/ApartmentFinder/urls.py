"""ApartmentFinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('tenant_home', views.tenant_home, name='tenant_home'),
    path('landlord_home', views.landlord_home, name='landlord_home'),

    path('roommate_form', views.roommate_form, name='roommate_form'),
    path('roommate_list', views.roommate_list, name='roommate_list'),
    path('good_roommate_list', views.good_roommate_list, name='good_roommate_list'),
    path('roommate_detail/<int:roommate_pk>', views.roommate_detail, name='roommate_detail'),

    path('apartment_form', views.apartment_form, name='apartment_form'),
    path('apartment_list', views.apartment_list, name='apartment_list'),
    path('apartment_detail/<int:apartment_pk>', views.apartment_detail, name='apartment_detail'),
]
