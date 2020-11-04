from django.shortcuts import render, redirect
from wall_app.models import User, Message, Comment
from django.contrib import messages

import bcrypt

# Create your views here.
def index(request):
    context = {
        'all_users':User.objects.all()
    }
    return render(request, "register_login.html", context)

def wall(request):
    if 'user_id' not in request.session:
        return redirect('/')
    
    context = {
        'all_messages': Message.objects.all().order_by('-created_at')
    }
    return render(request, "thewall.html", context)

def register(request):
     # include some logic to validate user input before adding them to the database!
    if request.method == "POST":
        errors = User.objects.validate_data(request.POST)
        if len(errors) > 0:
            for key, errormsg in errors.items():
                messages.error(request, errormsg)
            return redirect("/")
        else:
            password = request.POST['password_txt']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash    
            print(pw_hash)      # prints something like b'$2b$12$sqjyok5RQccl9S6eFLhEPuaRaJCcH3Esl2RWLm/cimMIEnhnLb7iC'    
            # be sure you set up your database so it can store password hashes this long (60 characters)
            # make sure you put the hashed password in the database, not the one from the form!
            new_user=User.objects.create(
                first_name=request.POST['first_name_txt'],
                last_name=request.POST['last_name_txt'],
                email=request.POST['email_txt'],
                password=pw_hash
            )
            request.session['user_id'] = new_user.id
            request.session['user_name'] = f'{new_user.first_name} {new_user.last_name}'
            return redirect("/wall") # never render on a post, always redirect!
    return redirect("/")

def login(request):
    if request.method =='POST':
        # see if the username provided exists in the database
        user = User.objects.filter(email=request.POST['email_txt']) # why are we using filter here instead of get?
        if user: # note that we take advantage of truthiness here: an empty list will return false
            logged_user = user[0]
            # assuming we only have one user with this username, the user would be first in the list we get back
            # of course, we should have some logic to prevent duplicates of usernames when we create users
            # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
            if bcrypt.checkpw(request.POST['password_txt'].encode(), logged_user.password.encode()):
                # if we get True after checking the password, we may put the user id in session
                request.session['user_id'] = logged_user.id
                request.session['user_name'] = f'{logged_user.first_name} {logged_user.last_name}'
                # never render on a post, always redirect!
                return redirect("/wall")
        # if we didn't find anything in the database by searching by username or if the passwords don't match, 
        # redirect back to a safe route
        return redirect("/")
    return redirect("/")

def newPost(request):
    if request.method =="POST":
        Message.objects.create(
            user = User.objects.get(id=int(request.session['user_id'])),
            content = request.POST['message_txt']
        )
        return redirect('/wall')
    return redirect('/')

def newComment(request):
    if request.method =="POST":
        Comment.objects.create(
            user = User.objects.get(id=int(request.session['user_id'])),
            message = Message.objects.get(id=int(request.POST['message_id'])),
            content = request.POST['comment_txt']
        )
        return redirect('/wall')
    return redirect('/')

def deleteMsg(request, message_id):
    if request.method == "POST":
        Message.objects.get(id=message_id).delete()
        return redirect("/wall")
    return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")