from django.db import models
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render,redirect
import bcrypt
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Wrong email address!"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"         
        return errors

    def basic_validator_reg(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field       
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"  
        if len(postData['confirmpassword']) < 8:
            errors["confirmpassword"] = "Confirm Password should be at least 8 characters" 
        if len(postData['lastname']) < 3:
            errors["lastname"] = "Last name should be at least 3 characters" 
        if len(postData['firstname']) < 3:
            errors["firstname"] = "First Name should be at least 3 characters" 
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Wrong email address!"
        if postData['password'] != postData['confirmpassword']:
            errors['password_confirm'] = "Password Dosent Match!"
        return errors

class TVShowManager(models.Manager):
    def basic_validator_reg_show(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field       
        if len(postData['title']) < 3:
            errors["title"] = "title should be at least 3 characters"  
        if len(postData['network']) < 3:
            errors["network"] = "network should be at least 3 characters" 
        if len(postData['description']) < 3:
            errors["description"] = "description should be at least 3 characters"        
        return errors

# Create your models here.
class User(models.Model):   
    firstname = models.TextField()
    lastname = models.TextField()
    email = models.CharField(max_length=45)
    password = models.TextField()
    login_date = models.DateTimeField() 
    objects = UserManager() 


class TVShow(models.Model): 
    title = models.TextField(null=True)
    network = models.TextField(null=True)
    description = models.TextField(null=True)
    birthDay = models.DateField(null=True)
    created_by = models.IntegerField(null=True)
    objects = TVShowManager()
    
class Likes(models.Model): 
    likes = models.IntegerField(null=True)
    likedby = models.IntegerField(null=True)

def user_login(formvalue): #request.POST   
        user_exist = User.objects.filter(email=formvalue.POST['email'])
        #print(user_exist.password)
        #print(formvalue.POST['password'].encode() )
        if user_exist:
            logged_user = user_exist[0] 
            if bcrypt.checkpw(formvalue.POST['password'].encode(), user_exist[0].password.encode()):
                print("password match")
                loggedin(formvalue,logged_user )
                return redirect('/app1/Viewall')
                #messages.success(formvalue, "User successfully Logged")
            else:
                print("failed password")   
                return False            
        else:
            #print(user_exist[0].password)
            print("testtttttt")
            return False   

def save_user(formvalue): #request.POST    
        user_password = formvalue.POST['password']
        hash1 = bcrypt.hashpw(user_password.encode(), bcrypt.gensalt()).decode()
        print(user_password)
        u = User.objects.create(email = formvalue.POST['email'] ,password = hash1 ,login_date=datetime.now(), firstname = formvalue.POST['firstname'], lastname = formvalue.POST['lastname'] )
        formvalue.session['email'] = u.email
        formvalue.session['loggedin'] = 1
        formvalue.session['firstname'] = u.firstname
        formvalue.session['lastname'] = u.lastname
        formvalue.session['user_id'] = u.id
        #messages.success(formvalue, "User successfully Saved")

def get_allshow():
    return TVShow.objects.all()


def save_show(formvalue): #request.POST       
        TVShow.objects.create(title = formvalue.POST['title'] ,network = formvalue.POST['network'] ,description = formvalue.POST['description'] , created_by = 1, birthDay =datetime.now() )
        #messages.success(formvalue, "Show successfully Added")

def loggedin(value, logged_user):
    value.session['email'] = value.POST['email']
    value.session['loggedin'] = 1
    value.session['firstname'] = logged_user.firstname
    value.session['lastname'] = logged_user.lastname
    value.session['user_id'] = logged_user.id

def get_show(show_id):
    return TVShow.objects.get(id=show_id)

def remove_show(show_id):
    TV_Show = TVShow.objects.get(id=show_id)
    TV_Show.delete()

def update_show(show_id):
    TV_Show = TVShow.objects.get(id=show_id)
    return TV_Show

def update_show_data(value): #request.POST
    TV_Show = TVShow.objects.get(id=value.POST['id'])
    TV_Show.title = value.POST['title']
    TV_Show.network = value.POST['network']
    TV_Show.description = value.POST['description']
    TV_Show.birthDay = value.POST['birthDay']
    
    #print("aaaaaaaaaaaaaa$$$$$$$$$$$",User2.username, User2.password, User2.login_date) 
    TV_Show.save()


def like_show(show_id,request):
    TV_Show = TVShow.objects.get(id=show_id)
    user_id = request.session['user_id']
    Likes.objects.create(likes = 1 ,likedby =  user_id )
    

def get_added_by(show_id):
    TV_show = TVShow.objects.get(id=show_id)
    User1 = User.objects.get(id=TV_show.id)
    print(User1.id)
    return User1.id
