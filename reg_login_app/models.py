from __future__ import unicode_literals
import re
from django.db import models

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(post_data['first_name']) < 1:
            errors['first_name'] = "Please provide a first name."
        if len(post_data['last_name']) < 1:
            errors['last_name'] = "Please provide a last name."
        if len(post_data['email']) < 1:
            errors['email'] = "Please provide a email."
        if not EMAIL_REGEX.match(post_data['email']):            
            errors['email'] = "Invalid email address!"
        if len(post_data['password']) < 1:
            errors['password'] = "Please provide a password."
        if post_data['pw_confirm'] != post_data['password']:
            errors['pw_confirm'] = "Password confirmation doesn't match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField()
    password = models.CharField(max_length = 64)
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
