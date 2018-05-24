from __future__ import unicode_literals
from django.db import models
import re
from importlib import import_module
from django.conf import settings
import bcrypt
from bcrypt import checkpw
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class userManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["fname"] = "User first name should be more than 1 character"
        elif postData['first_name'].isalpha() == False:
            errors["fname"] = "Invalid first name"
        if len(postData['last_name']) < 2:
            errors['lname'] = "User last name should be more than 1 character"
        elif postData['last_name'].isalpha() == False:
            errors["lname"] = "Invalid first name"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "invalid email"
        else:
            matched_email = users.objects.filter(email = postData['email'])
            if len(matched_email) > 0:
                errors['email'] = "invalid email"
            else:
                print("email is not in db")
        if postData['password'] != postData['confirm']:
            errors['confirm'] = "passwords must match"
        if len(postData['password'])<8:
            errors['password'] = 'password too short'
        return errors
    def login_validator(self,postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "cannot match email"
            errors['password'] = 'cannot match password'
        else:
            matched_email = users.objects.filter(email = postData['email'])
            #print(matched_email[0].email)
            if len(matched_email) > 0:
                print('matched email')
                if checkpw(postData['password'].encode(), matched_email[0].pw_hash.encode()):
                    print('matched password')
                else:
                    errors['email'] ='cannot validate your username'                        
                    errors['password'] ='cannot validate your password'
            else:
                errors['email'] = 'register yo email'
        return errors
    def edit_validator(self,postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["fname"] = "User first name should be more than 1 character"
        elif postData['first_name'].isalpha() == False:
            errors["fname"] = "Invalid first name"
        if len(postData['last_name']) < 2:
            errors['lname'] = "User last name should be more than 1 character"
        elif postData['last_name'].isalpha() == False:
            errors["lname"] = "Invalid first name"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "invalid email"
        else:
            matched_email = users.objects.filter(email = postData['email']).exclude(id = postData['id'])
            if len(matched_email) > 0:
                errors['email'] = "invalid email"
            else:
                print("email is not in db")
        return errors
class quoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if len(postData['quotee']) < 4:
            errors['quotee'] = 'not pretentious enough'
        if len(postData['quote']) < 11:
            errors['quote'] = 'not pretentious enough'
        return errors
class users(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()
    def __repr__(self):
        return "<user object: name: {} {} email: {}".format(self.fname, self.lname, self.email)

class quotes(models.Model):
    quotee = models.CharField(max_length=255)
    quote = models.CharField(max_length=255)
    poster = models.ForeignKey(users, related_name = "quotes")
    users_liked = models.ManyToManyField(users, related_name = "likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = quoteManager()
    def __repr__(self):
        return "<quote object: quotee: {} quote: {}".format(self.quotee, self.quote)
