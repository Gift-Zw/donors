import threading

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_control

from .admin import UserCreationForm
from .models import User, Beneficiary, OnlineDonation
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import BeneficiaryRegistrationForm, OnlineDonationForm
from .decorators import admin_required
from .emails import send_thank_you_email, send_donation_received_email, send_anonymous_donation_received_email


# Create your views here.

class UserRegistrationView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'register_user.html'
    success_url = reverse_lazy('add-beneficiary')

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = User.objects.get(email=email)
        login(self.request, user)
        return redirect('add-beneficiary')


class UserLoginView(LoginView):
    template_name = 'user_login.html'

    def get_success_url(self):
        if Beneficiary.objects.filter(manager=self.request.user).exists():
            return reverse_lazy('manager-dashboard')
        else:
            return reverse_lazy('add-beneficiary')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_logout_view(request):
    logout(request)
    return redirect('dashboard')


def dashboard_view(request):
    donations = OnlineDonation.objects.order_by('-date')[:5]
    context = {
        'donations': donations,
        'orphanages_total': Beneficiary.objects.filter(category='Orphanage').count(),
        'old_homes_total': Beneficiary.objects.filter(category='Old Peoples Home').count(),
        'beneficiary_total': Beneficiary.objects.all().count()
    }
    return render(request, 'index.html', context)


@admin_required()
def manager_dashboard_view(request):
    beneficiary = Beneficiary.objects.filter(manager=request.user).first()
    context = {
        'beneficiary': beneficiary,
        'paypal_total': OnlineDonation.objects.filter(payment_method='Paypal', beneficiary=beneficiary).count(),
        'credit_card': OnlineDonation.objects.filter(payment_method='Credit Card', beneficiary=beneficiary).count(),
        'bank_transfer': OnlineDonation.objects.filter(payment_method='Bank Transfer', beneficiary=beneficiary).count(),
        'ecocash': OnlineDonation.objects.filter(payment_method='Ecocash', beneficiary=beneficiary).count(),
        'usd_total': OnlineDonation.objects.filter(currency='USD', beneficiary=beneficiary).count(),
        'zig_total': OnlineDonation.objects.filter(currency='ZiG', beneficiary=beneficiary).count(),
        'zar_total': OnlineDonation.objects.filter(currency='ZAR', beneficiary=beneficiary).count(),
        'donations': OnlineDonation.objects.filter(beneficiary=beneficiary)[:5]
    }
    return render(request, 'manager_dash.html', context)


@admin_required()
def manager_donations_view(request):
    beneficiary = Beneficiary.objects.filter(manager=request.user).first()
    donations = OnlineDonation.objects.filter(beneficiary=beneficiary)
    context = {
        'beneficiary': beneficiary,
        'donations': donations
    }
    return render(request, 'manager_donations.html', context)


@admin_required()
def manager_profile_view(request):
    beneficiary = Beneficiary.objects.filter(manager=request.user).first()
    recent_donations = OnlineDonation.objects.filter(beneficiary=beneficiary)
    context = {
        'beneficiary': beneficiary,
        'recent_donations': recent_donations
    }
    return render(request, 'manager_profile.html', context)


def donations_view(request):
    donations = OnlineDonation.objects.all()
    context = {
        'donations': donations
    }
    return render(request, 'online_donations.html', context)


def orphanages_view(request):
    orphanages = Beneficiary.objects.filter(category='Orphanage')
    context = {
        'orphanages': orphanages
    }
    return render(request, 'orphanages.html', context)


def old_peoples_home_view(request):
    old_peoples_homes = Beneficiary.objects.filter(category='Old Peoples Home')
    context = {
        'old_homes': old_peoples_homes
    }
    return render(request, 'old_people_homes.html', context)


def beneficiary_profile_view(request, id):
    beneficiary = Beneficiary.objects.filter(id=id).first()
    if request.method == 'POST':
        form = OnlineDonationForm(request.POST)
        if form.is_valid():
            print('heyyyy')
            try:
                test = form.data['donor_name']
                donation = OnlineDonation.objects.create(
                    beneficiary=beneficiary,
                    amount=form.data['amount'],
                    currency=form.data['currency'],
                    payment_method=form.data['payment_method'],
                    donor_name=form.data['donor_name'],
                    donor_email=form.data['donor_email'],
                    donor_cell=form.data['donor_cell']
                )
                donation.save()
                send_donation_received_email(donation)
                send_thank_you_email(donation)
            except:
                donation = OnlineDonation.objects.create(
                    beneficiary=beneficiary,
                    amount=form.data['amount'],
                    currency=form.data['currency'],
                    payment_method=form.data['payment_method'],
                )
                donation.save()
                send_anonymous_donation_received_email(donation)
            return redirect('profile', beneficiary.id)
        else:
            pass
    else:
        form = OnlineDonationForm()

    context = {
        'beneficiary': beneficiary,
        'form': OnlineDonationForm(),
        'donations': OnlineDonation.objects.filter(beneficiary=beneficiary)
    }
    return render(request, 'beneficiary_profile.html', context)


@admin_required()
def register_beneficiary_view(request):
    if request.method == 'POST':
        form = BeneficiaryRegistrationForm(request.POST)
        files = request.FILES.getlist('files')
        if form.is_valid():
            beneficiary = Beneficiary.objects.create(
                category=form.data['category'],
                email=form.data['email'],
                city=form.data['city'],
                name=form.data['name'],
                address=form.data['address'],
                cell=form.data['cell'],
                about=form.data['about'],
                latitude=form.data['latitude'],
                longitude=form.data['longitude'],
                manager=request.user
            )
            beneficiary.save()
            logo = form.cleaned_data['logo']
            cover_image = form.cleaned_data['cover_image']
            if logo:
                beneficiary.logo = logo
                beneficiary.save()
            if cover_image:
                beneficiary.cover_image = cover_image
                beneficiary.save()

            return redirect('manager-dashboard')
        else:
            messages.error(request, form.errors)

    else:
        form = BeneficiaryRegistrationForm()
    context = {
        'form': form,
    }

    return render(request, 'create_beneficiary.html', context)
