from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request,f'You have created a user account for {username}!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    context = {'form':form}
    return render(request, 'users/register.html', context)


def profile(request):
    return render(request, 'users/profile.html')