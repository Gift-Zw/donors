"""
URL configuration for donors project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from core.views import dashboard_view, donations_view, orphanages_view, old_peoples_home_view, beneficiary_profile_view, \
    UserLoginView, UserRegistrationView, register_beneficiary_view, manager_dashboard_view, manager_donations_view, manager_profile_view, user_logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_view, name="dashboard"),
    path('online-donations/', donations_view, name="online-donations"),
    path('orphanages/', orphanages_view, name="orphanages"),
    path('old-peoples-homes/', old_peoples_home_view, name="old-peoples-homes"),
    path('profile/<int:id>/', beneficiary_profile_view, name="profile"),
    path('register/', UserRegistrationView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', user_logout_view, name="logout"),
    path('add-beneficiary/', register_beneficiary_view, name="add-beneficiary"),
    path('manager-dashboard/', manager_dashboard_view, name="manager-dashboard"),
    path('manager-donations/', manager_donations_view, name="manager-donations"),
    path('manager-profile/', manager_profile_view, name="manager-profile"),
]
