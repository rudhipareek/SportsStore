from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration Successful!')
            return redirect('home') 
        else:
            messages.error(request, 'Registration Failed') 
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
     logout(request)
     messages.success(request, "You have been logged out successfully!")
     return redirect('home') 
    else:
        messages.error(request, "Invalid logout attempt.")
        return redirect('home') 