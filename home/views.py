from django.shortcuts import render

def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    return render(request, 'home/contact.html')


########
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def logout_confirm_view(request):
    return render(request, 'account/logout.html')  # This is the logout confirmation page

