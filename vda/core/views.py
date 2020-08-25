from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import subprocess
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from core.models import Guestbook
from django.utils import timezone
import configparser

config = configparser.ConfigParser()
config.read('core/static/core/navinfo.ini')

def index(request):
    context = { "navinfo": config['DEFAULT']['Index'] }
    return render(request, 'core/index.html', context)

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
    return render(request, 'registration/signup.html', {"form":form})

def profile(request):
    return render(request, 'user/profile.html', None)

def testconn(request):
    context = { "navinfo": config['DEFAULT']['CommandExec'] }
    if request.method == 'POST':
        webAddr = request.POST.get('serveraddr')
        procOut = subprocess.check_output('powershell.exe Test-Connection ' + webAddr, shell=True)
        context = { 
            "stdout": procOut.decode(),
            "navinfo": config['DEFAULT']['CommandExec']
        }
        return render(request, 'utils/testconn.html', context)
    return render(request, 'utils/testconn.html', context)

@csrf_exempt
def changepass(request):
    context = { "navinfo": config['DEFAULT']['CSRF'] }
    if request.method == 'POST':
        password1 = request.POST.get('newpass1')
        password2 = request.POST.get('newpass2')
        if (password1 == password2):
            context = { "msg": 'Your new password is ' + password1,
                        "navinfo": config['DEFAULT']['CSRF']
            }
        else:
            context = { "msg": 'Passwords did not match.',
                        "navinfo": config['DEFAULT']['CSRF']
             }
        return render(request, 'user/changepass.html', context)
    return render(request, 'user/changepass.html', context)

def filerunner(request):
    if request.method == 'GET':
        file = request.GET.get('file')
        if (file):
            procOut = subprocess.check_output(['python', file], shell=True)
            context = { 
                "stdout": procOut.decode(),
                "file1": "dt.py",
                "file2": "version.py",
                "file3": "fibonacci.py",
                "navinfo": config['DEFAULT']['FileInclusion']
            }
            return render(request, 'utils/filerunner.html', context)
    context = {
        "file1": "dt.py",
        "file2": "version.py",
        "file3": "fibonacci.py",
        "navinfo": config['DEFAULT']['FileInclusion']
    }
    return render(request, 'utils/filerunner.html', context)

def userlookup(request):
    context = { "navinfo": config['DEFAULT']['SQLi'] }
    if request.method == 'POST':
        uname = request.POST.get('uname')
        query = User.objects.raw('SELECT * from "auth_user" WHERE "auth_user"."username" = "' + uname + '"')
        context = { "stdout": query,
                    "navinfo": config['DEFAULT']['SQLi']
        }
        return render(request, 'utils/userlookup.html', context)
    return render(request, 'utils/userlookup.html', context)

def guestbook(request):
    
    if request.method == 'POST':
        uname = request.POST.get('uname')
        umsg = request.POST.get('umsg')
        gbook = Guestbook(first_name=uname, user_message=umsg, pub_date=timezone.now())
        gbook.save()
    posts = Guestbook.objects.all()
    if posts:
        context = { "posts": posts,
                    "navinfo": config['DEFAULT']['XSSs']
        }
    else:
        context = { "navinfo": config['DEFAULT']['XSSs'] }
    return render(request, 'utils/guestbook.html', context)