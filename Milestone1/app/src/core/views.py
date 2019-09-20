from django.shortcuts import render, redirect
from . import models
from . import forms


def home(request):
    return render(request, 'home.html', {})


def tenant_home(request):
    user = request.COOKIES.get('roommmate')
    # You're already a roommate
    if user is not None:
        user = models.RoommateApplication.objects.get(pk=user)
        request.session['user'] = user
        request.session.save()
        return render(request, 'tennant_home.html', {
            'user': user,
        })
    # Become a roommate
    return redirect('roommate_form')


def landlord_home(request):
    return render(request, 'landlord_home.html', {})


def roommate_form(request):
    if request.method == 'POST':
        form = forms.RoommateForm(request.POST)
        if form.is_valid():
            roommate = form.save(commit=True)
            request.COOKIES['roommate'] = roommate.pk
            return redirect('roommate_list')
    else:
        form = forms.RoommateForm()

    return render(request, 'roommate_form.html', {
        'form': form,
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
    })
