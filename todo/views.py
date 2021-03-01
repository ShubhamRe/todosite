from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required #to access page only if we are logged in

from .forms import Todoform
from .models import Todo

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
    #todos = Todo.objects.all() # to get all the todo objects.
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True) #to get only user specific todo objects whose datecompleted is null.
    return render(request, 'todo/currenttodos.html',{'todos':todos})

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
            # return render(request, 'todo/currenttodos.html')
            return redirect('currenttodos')

@login_required #accessible only if user is logged in
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required #accessible only if user is logged in
def createtodos(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'createtodoform': Todoform()})
    else:
        try:
            form = Todoform(request.POST)
            newtodo = form.save(commit=False) #commit =false is bcoz we dont want to save this todo object directly in database we have to assing it to variable newtodo.
            newtodo.user = request.user # so that one user can not touch other user todos.
            newtodo.save() # now it will save in database.
            return redirect('currenttodos')
        except ValueError: #if user enters more value than capacity then this exception will come.so we show error message.
            return render(request, 'todo/createtodo.html', {'createtodoform': Todoform(),'error':'Bad data entered.'})

@login_required #accessible only if user is logged in
def viewtodos(request,todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk,user=request.user) # to display todo of that particualr id given in url of that particular user.
    if request.method == 'GET':
        form = Todoform(instance=todo)# this is to display all the todo details in form format hence we create object and pass it into dictionary and that same dictionary used in viewtodos.html
        return render(request, 'todo/viewtodos.html',{'todos':todo,'form':form})
    else:
        try:
            form = Todoform(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodos.html', {'todos': todo, 'error': 'Bad data entered.'})

@login_required #accessible only if user is logged in
def completetodos(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk,user=request.user)  # to complete todo of that particualr id given in url of that particular user.
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required #accessible only if user is logged in
def deletetodos(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk,user=request.user)  # to delete todo of that particualr id given in url of that particular user.
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

@login_required #accessible only if user is logged in
def completedtodos(request):
    #todos = Todo.objects.all() # to get all the todo objects.
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') #to get only user specific todo objects whose datecompleted is not null and order by datecompleted (here we ahve used - to get descendong order for ascending don't use -) if we use - then it will show recent todo first ..
    return render(request, 'todo/completedtodos.html',{'todos':todos})


def apiOverview(request):
    return JsonResponse("API BASE POINT",safe=False)