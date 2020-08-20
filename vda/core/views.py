from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import subprocess
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'core/index.html', None)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def profile(request):
    return render(request, 'user/profile.html', None)

def testconn(request):
    if request.method == 'POST':
        webAddr = request.POST.get('serveraddr')
        procOut = subprocess.check_output('powershell.exe Test-Connection ' + webAddr, shell=True)
        context = { "stdout": procOut.decode() }
        return render(request, 'utils/testconn.html', context)
    return render(request, 'utils/testconn.html', None)

@csrf_exempt
def changepass(request):
    if request.method == 'POST':
        password1 = request.POST.get('newpass1')
        password2 = request.POST.get('newpass2')
        if (password1 == password2):
            context = { "msg": 'Your new password is ' + password1 }
        else:
            context = { "msg": 'Passwords did not match.' }
        return render(request, 'user/changepass.html', context)
    return render(request, 'user/changepass.html', None)