from __future__ import unicode_literals
from django.db import models
import bcrypt, re


# Create your models here.
class UserManager(models.Manager):
    def registration_validator(self, post_data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(post_data['name']) < 2:
            errors['name'] = 'Please enter a name.'
        if len(post_data['alias']) < 2:
            errors['alias'] = 'Please enter a alias.'
        if len(post_data['email']) < 1:
            errors['email'] = 'Please enter an email address.'
        elif not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Please enter a valid email address.'
        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters.'
        if post_data['confirmed_password'] != post_data['password']:
            errors['confirmed_password'] = 'Password is not confirmed.'
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors['email'] = 'Email address already registered.'
        return errors
    
    def login_validator(self, post_data):
        errors = {}
        logged_user = User.objects.filter(email=post_data['email'])
        if len(post_data['email']) < 1:
            errors['email'] = 'Please enter an email address.'
        if len(post_data['password']) < 1:
            errors['password'] = 'Please enter a password.'
        if len(User.objects.filter(email=post_data['email'])) == 0:
            errors['email'] = 'Email has not been registered.'
            return errors
        else:
            logged_user = User.objects.filter(email=post_data['email'])[0]
            print(logged_user.password)
        if bcrypt.checkpw(post_data['password'].encode('UTF-8'), logged_user.password.encode('UTF-8')):
            pass
        else:
            errors['password'] = 'Incorrect password.'
        return errors
    
   

class User(models.Model):
    name = models.CharField(max_length=255)
    alias= models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)    
    objects = UserManager()

class PokeManager(models.Manager):
    def Poke(self, id, uid):
        try:
            userToPoke =User.objects.get(id=id)
            loggedUser=User.objects.get(id=uid)
            Poke.objects.create(poker=loggedUser, pokie=userToPoke)
        except:
            print("No user with id {}".format(id))
        
class Poke(models.Model):
    poker = models.ForeignKey(User, related_name="poker", on_delete=models.PROTECT)
    pokie = models.ForeignKey(User, related_name="pokie", on_delete=models.PROTECT)
    created_at = models.DateField(null=True)
    counter = models.IntegerField(blank=False, default=0, null=True)
    total_pokes = models.IntegerField(blank=False, default=0, null=True)
    objects = PokeManager()