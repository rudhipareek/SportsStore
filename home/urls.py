from django.urls import path
from . import views
from .views import logout_confirm_view
from allauth.account.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('logout/', logout_confirm_view, name='account_logout_confirm'),  # Confirmation Page
    path('logout/confirm/', LogoutView.as_view(), name='account_logout'),  # Actual Logout
]
