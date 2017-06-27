# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login_app.models import User
from datetime import datetime

class PlanManager(models.Manager):
    # Clears db
    def delete_all(self):
        User.objects.all().delete()
        Plan.objects.all().delete()

    # Checks to see if user input for new plan is valid
    def validate_plan(self, postData, results, date_from, date_to):
        # Checks to see if destination is filled out
        if not postData['destination']:
            results['valid'] = False
            results['errors'].append("Please enter a destination.")
        # Checks to see if description is filled out
        if not postData['description']:
            results['valid'] = False
            results['errors'].append("Please enter a description.")
        # Checks if date from is filled out
        if not postData['date_from']:
            results['valid'] = False
            results['errors'].append("Please enter a valid entry for date from.")
        # Checks if date to is filled out
        if not postData['date_to']:
            results['valid'] = False
            results['errors'].append("Please enter a valid date for date to.")
        # Checks if dates don't overlap
        elif postData['date_from'] > postData['date_to']:
            results['valid'] = False
            results['errors'].append("Please have the starting date be before the ending date.")
    
        # Checks if both dates are in the future
        if date_from < datetime.now().date():
            results['valid'] = False
            results['errors'].append("Please enter a starting date that's not in the past.")
        if date_to < datetime.now().date():
            results['valid'] = False
            results['errors'].append("Please enter an ending date that's not in the past.")
        return results

    # Creates a new plan if user input is valid
    def create_plan(self, postData, current_user):
        results = {'valid': True, 'errors': [], 'user': None}
        # If dates are valid, check the rest and create object
        try:
            date_from = datetime.strptime(postData['date_from'], '%Y-%m-%d').date()
            date_to = datetime.strptime(postData['date_to'], '%Y-%m-%d').date()
            results = self.validate_plan(postData, results, date_from, date_to)

            all_plans = Plan.objects.all()
        
            if results['valid']:
                Plan.objects.create(
                    destination=postData['destination'],
                    description=postData['description'],
                    date_from=date_from,
                    date_to=date_to,
                    owner_id=current_user
                )
        # If not, give error and return
        except:
            results['valid'] = False
            results['errors'].append("The date fields are either not completely filled \
            out or one of the dates is to far in the future (year has more than 4 digits).")
        return results

# Model: Plan
class Plan(models.Model):
    destination = models.CharField(max_length=75)
    description = models.CharField(max_length=100)
    date_from = models.DateField()
    date_to = models.DateField()
    owner_id = models.ForeignKey(User)
    others = models.ManyToManyField(User, related_name="plans")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PlanManager()
