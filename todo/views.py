from django.db import IntegrityError
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate

# Create your views here.
def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request,'todo/signupuser.html',{'signupform':UserCreationForm()}) # Here in dictionary we have used
# UserCreationForm() this is inbuilt from django when we want to use user authentication then we can simply use it by
# importing its respective library(from django.contrib.auth.forms import UserCreationForm) and show it on html page

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])# we can use any password
                # password1 or password2 here we are using password1.
                user.save() # to save newly created user in database not sql db but db accessible under /admin.
                login(request,user) # after sign up we have to login the user.
                return redirect('currenttodos') # and after user gets logged in in app then we have to take the user to current todos page hence we have called currenttodos function.
            except IntegrityError: # IntegrityError is becoz if we creating user with already used username then this exception will get generated, so in this case we have to show message and keep user to same signup page.
                return render(request, 'todo/signupuser.html',{'signupform': UserCreationForm(), 'error': 'Username already used. Please choose a new Username'})
        else:
            return render(request,'todo/signupuser.html',{'signupform':UserCreationForm(),'error':'Passwords did not match'}) # if password1 and password2 did not match then we have to show proper error message.

def currenttodos(request):
    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
    login(request, user)
    return render(request, 'todo/currenttodos.html')

def loginuser(request):
    # this means we are logging in using <a> tag and <a> tag uses GET request so if login from <a>
    # then we are redirecting to loginuser.html page and from then by giving username and password we are loggin in using login button(i.e form using POST method)
    # then code will go to else loop and user will get authenticate using authenticate function. and if in case user values did not matched or if its none
    # then we are returning error message as Username and Password did not match.
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html',{'loginform': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'loginform': AuthenticationForm(),'error':'Username and Password did not match.'})
        else:
            login(request, user)
            return render(request, 'todo/currenttodos.html')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')