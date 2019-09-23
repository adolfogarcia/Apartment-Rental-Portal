from django.shortcuts import render, redirect
from . import models
from . import forms


def home(request):
    return render(request, 'home.html', {})


def tenant_home(request):
    user_pk = request.session.get('user')

    # You're already a roommate
    if user_pk is not None:
        user = models.RoommateApplication.objects.get(pk=user_pk)
        return render(request, 'tenant_home.html', {
            'user': user,
        })

    # Become a roommate
    return redirect('roommate_form')


def landlord_home(request):
    return redirect('apartment_form')


def roommate_form(request):
    if request.method == 'POST':
        form = forms.RoommateForm(request.POST)
        if form.is_valid():
            roommate = form.save(commit=True)
            request.session['user'] = roommate.pk
            request.session.save()

            return redirect('tenant_home')
    else:
        form = forms.RoommateForm()

    return render(request, 'roommate_form.html', {
        'form': form,
    })


def good_roommate_list(request):
    user_pk = request.session.get('user')
    if user_pk is not None:
        user = models.RoommateApplication.objects.get(pk=user_pk)
    else:
        user = None

    roommates = models.RoommateApplication.objects.exclude(pk=user_pk)

    # Find similar roommates
    roommates = roommates.filter(
        gender=user.looking_for_gender,
        cleanliness=user.cleanliness,
        year=user.year,
        smoking=user.smoking,
    )

    return render(request, 'roommate_list.html', {
        'user': user,
        'roommates': roommates,
    })


def roommate_list(request):
    user_pk = request.session.get('user')
    if user_pk is not None:
        user = models.RoommateApplication.objects.get(pk=user_pk)
    else:
        user = None

    roommates = models.RoommateApplication.objects.exclude(pk=user_pk)

    return render(request, 'roommate_list.html', {
        'user': user,
        'roommates': roommates,
    })


def roommate_detail(request, roommate_pk):
    return render(request, 'roommate_detail.html', {
        'roommate': models.RoommateApplication.objects.get(pk=roommate_pk)
    })


def apartment_form(request):
    if request.method == 'POST':
        form = forms.ApartmentForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('apartment_list')
    else:
        form = forms.ApartmentForm()

    return render(request, 'apartment_form.html', {
        'form': form,
        'tenants': models.RoommateApplication.objects.all(),
    })


def apartment_list(request):
    user_pk = request.session.get('user')
    if user_pk is not None:
        user = models.RoommateApplication.objects.get(pk=user_pk)
    else:
        user = None

    apartments = models.Apartment.objects.all()

    return render(request, 'apartment_list.html', {
        'user': user,
        'apartments': apartments,
    })


def apartment_detail(request, apartment_pk):
    return render(request, 'apartment_detail.html', {
        'apartment': models.Apartment.objects.get(pk=apartment_pk),
    })
