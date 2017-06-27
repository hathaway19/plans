# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from ..login_app.models import User
from .models import Plan
from datetime import datetime
# Create your views here.
def index(request):
    # If we can't get the current user, navigate back to login page
    try:
        current_user = User.objects.get(id=request.session['login_id'])
    except:
        print "User is not logged in"
        return redirect(reverse('login_app:logout'))

    # Holds all plans and Users in db
    all_users = User.objects.all()
    all_plans = Plan.objects.all()

    # Plan.objects.all().delete()
    # User.objects.all().delete()

    joining = [] #array to hold the plans that user will be joining (not their own)
    for plan in all_plans:
        if plan in current_user.plans.all():
             joining.append(plan.id)

    context = {
        'users': all_users,
        'current_user': current_user,
        'all_plans': all_plans,
        'joining': joining
    }
    return render(request, 'belt_app/index.html', context)

# Page to create new plan
def add(request):
    return render(request, 'belt_app/add.html')

# Validates user input and creates a new plan if valid
def add_trip(request):
    # If user not logged in, navigate back to login screen
    try:
        # get the user trying to make the review
        current_user = User.objects.get(id=request.session['login_id'])
    except:
        # Logs out if user id can't be found
        print "User is not logged in"
        return redirect(reverse('login_app:logout'))

    # Get the results from models
    results = Plan.objects.create_plan(request.POST, current_user)

    # If valid go to home screen
    if results['valid']:
        return redirect(reverse('belt_app:index'))
    # If not a valid entry, show errors and reload current page
    for error in results['errors']:
        messages.error(request, error)
    return redirect(reverse('belt_app:add'))

# Shows an individual plan based on id
def show_plan(request, id):
    # Get the plan in question, if it doesn't exist, go to home page
    try:
        current_plan = Plan.objects.get(id=id)
    except:
        print "Plan doesn't exist"
        return redirect(reverse('belt_app:index'))

    context = {
        'plan': current_plan,
        'attendees': current_plan.others.all() # people planning to attend that event (not the host)
    }
    return render(request, 'belt_app/show.html', context)

# Adds user to plan if not already on it
def join_plan(request, join_id):
    # Gets current user
    try:
        # get the user trying to make the review
        current_user = User.objects.get(id=request.session['login_id'])
    except:
        # Logs out if user id can't be found
        print "User is not logged in"
        return redirect(reverse('login_app:logout'))
    # Get current plan
    try:
        current_plan = Plan.objects.get(id=join_id)
    except:
        print "Plan doesn't exist"
        return redirect(reverse('belt_app:index'))

    # Adds user to plan
    current_plan.others.add(current_user)

    # Go back to home
    return redirect(reverse('belt_app:index'))