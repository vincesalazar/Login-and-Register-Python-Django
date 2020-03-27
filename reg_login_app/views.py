from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User

def index(request):
    return render(request, 'index.html')

def register(request):
    post = request.POST
    errors = User.objects.basic_validator(post)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    lowerCaseEmail = post['email'].lower()
#     CHECKING TO SEE IF EMAIL IS ALREADY IN DATABASE
    if User.objects.filter(email = lowerCaseEmail).exists():
        messages.error(request, "That email already exists")
        return redirect('/')
    capitalizedFirstName = post['first_name'].capitalize()
    capitalizedLastName = post['last_name'].capitalize()
    password = post['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
#     CREATING USER
    user = User.objects.create(
        first_name = capitalizedFirstName, 
        last_name = capitalizedLastName, 
        email = lowerCaseEmail, 
        password = pw_hash
    )
    request.session['user_id'] = user.id

    return redirect('/success')

def login(request):
    post = request.POST
    lowerEmail = post['email'].lower()
    try:
        user = User.objects.get(email = lowerEmail)
    except:
        messages.error(request, "Please check your password or email.")
        return redirect('/')

    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session["user_id"] = user.id
        return redirect('/success')
    else:
        messages.error(request, "please check your password or email.")
        return redirect('/')
    
def success(request):
# MAKING SURE A USER WHOS LOGGED OUT HAS TO LOG BACK IN. SECURITY PURPOSE
    if "user_id" not in request.session:
        messages.error(request, "Must be logged in")
        return redirect('/')
    user_id = request.session['user_id']
    context = {
        "user": User.objects.get(id=user_id)
    }
    return render(request, "success.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')
