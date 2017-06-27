# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt, re # Libraries for hashing passwords and for validating strings

# Pattern needed to contain a valid email
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    # Creates acount after checking for valid information
    def register(self, postData):
        print postData
        results = {'valid': True, 'errors': [], 'user': None}
        # Name
        if not postData['name'] or len(postData['name']) < 3:
            results['valid'] = False
            results['errors'].append("Please enter a name that is at least 3 characters.")
        elif len(postData['name']) > 75:
            results['valid'] = False
            results['errors'].append("Please enter a name that is less than 76 characters")

        # Username
        if not postData['username'] or len(postData['username']) < 3:
            results['valid'] = False
            results['errors'].append("Please enter a username that is at least 3 characters.")
        elif len(postData['username']) > 75:
            results['valid'] = False
            results['errors'].append("Please enter a username that is less than 76 characters")

        # Email
        if not postData['email']:
            results['valid'] = False
            results['errors'].append("Please enter your email address.")
        elif len(postData['email']) > 64:
            results['valid'] = False
            results['errors'].append("Please enter an email that is less than 100 characters")
        # Check for valid email pattern
        elif not EMAIL_PATTERN.match(postData['email']):
            results['valid'] = False
            results['errors'].append("The provided email is not valid. Please enter a valid email (example: user@gmail.com).")

        # Passwords
        if not postData['password'] or len(postData['password']) < 8:
            results['valid'] = False
            results['errors'].append("Please enter a password with 8 or more characters.")
        elif len(postData['password']) > 75:
            results['valid'] = False
            results['errors'].append("Please enter a password that is less than 76 characters")
        # Checks to see if passwords are the same
        if postData['password'] != postData['confirm_password']:
            results['valid'] = False
            results['errors'].append("Please confirm that your two passwords match.")
        # # Makes sure the email doesn't already exist in db
        if User.objects.filter(email=postData['email']).exists():
            results['valid'] = False
            results['errors'].append("There is already an existing user with that email address.")
        # Creates user if results are valid
        else:
            if results['valid']:
                # hash the password for security purposes
                hashed_password = bcrypt.hashpw(str(postData['password']), bcrypt.gensalt())
                new_user = User.objects.create(
                    name=postData['name'],
                    username=postData['username'],
                    email=postData['email'],
                    password=hashed_password
                )
                results['user'] = new_user
        return results

    # For logging in with an existing acount
    def login(self, postData):
        results = {'valid': True, 'errors': [], 'user': None}
        # Checks to see if user email exists in db
        try:
            results['user'] = User.objects.get(email=postData['email'])
        # Not a valid acount if the email doesn't exist
        except:
            results['valid'] = False
            results['errors'].append("There is no user with that email and password.")
            return results
        # If passwords don't match, not a valid acount
        if  str(results['user'].password) != bcrypt.hashpw(str(postData['password']), str(results['user'].password)):
            results['valid'] = False
            results['errors'].append("There is no user with that email and password.")
        # Return the results
        return results

# Model for user acounts
class User(models.Model):
    name = models.CharField(max_length=75)
    username = models.CharField(max_length=75)
    password = models.CharField(max_length=75)
    email = models.CharField(max_length=75)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
