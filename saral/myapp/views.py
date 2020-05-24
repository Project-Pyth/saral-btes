import datetime
from operator import attrgetter
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.db import transaction
from myapp.forms import EditProfileForm, PersonalEditForm, NotificationForm, PersonalForm, LeaveApplyForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.
from myapp.models import UserProfile, Department, Notification, Personalnote, LeaveApply

posts_per_page = 8


# index page
def index(request):
    return render(request, 'index.html')


# Contact Us
def contact(request):
    return render(request, 'contact.html')


# developer Information
def devinfo(request):
    return render(request, 'devinfo.html')


# page rendered after login
@login_required(login_url='myapp:login')
def dashboard(request):
    context = {}

    posts = sorted(Notification.objects.filter(status=True), key=attrgetter('Date'), reverse=True)
    pro = UserProfile.objects.get(id=request.user.userprofile.id)
    context['pro'] = pro

    # pagination
    page = request.GET.get('page', 1)
    posts_paginator = Paginator(posts, posts_per_page)
    try:
        posts = posts_paginator.page(page)
    except PageNotAnInteger:
        posts = posts_paginator.page(posts_per_page)
    except EmptyPage:
        posts = posts_paginator.page(posts_paginator.num_pages)

    context['posts'] = posts

    return render(request, 'dashboard.html', context)


# Employee Login
def login(request):
    if request.method == 'POST':
        un = request.POST['user']
        pass1 = request.POST['password']

        user = auth.authenticate(username=un, password=pass1)
        if user is not None:
            auth.login(request, user)
            request.session['username'] = un
            request.session['id'] = user.id

            return redirect('myapp:dashboard')
        else:
            messages.info(request, 'Invalid Credentials!!')
            return redirect('myapp:login')
    else:
        return render(request, 'login.html')

@login_required(login_url='myapp:login')
def logout(request):
    auth.logout(request)

    return redirect('myapp:index')


# Saved User Profile
@login_required(login_url='myapp:login')
def view_profile(request, pk=None):
    context = {}
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        pro = UserProfile.objects.get(id=request.user.userprofile.id)
        start = datetime.datetime.now()
        end = start - datetime.timedelta(days=60)

        context['user'] = user
        context['pro'] = pro
        return render(request, 'profile.html', context)


# leaves approved by manager is shown to employee who sent it
@login_required(login_url='myapp:login')
def view_approve(request):
    context = {}
    leaves = LeaveApply.objects.filter(status=True, user=request.user).order_by('-date')
    page = request.GET.get('page', 1)
    posts_paginator = Paginator(leaves, posts_per_page)
    try:
        leaves = posts_paginator.page(page)
    except PageNotAnInteger:
        leaves = posts_paginator.page(posts_per_page)
    except EmptyPage:
        leaves = posts_paginator.page(posts_paginator.num_pages)

    context['leaves'] = leaves
    return render(request, 'approved-leaves.html', context)


# Edit User's Profile
@login_required(login_url='myapp:login')
@transaction.atomic
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=request.user)
        profile_form = PersonalEditForm(request.POST or None, request.FILES or None, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is successfully updated!!')
            user_form = EditProfileForm()
            profile_form = PersonalEditForm()
        else:
            messages.error(request, 'Please fill the correct Details!!')
    else:
        user_form = EditProfileForm(instance=request.user)
        profile_form = PersonalEditForm(instance=request.user.userprofile)
    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# Official Notification
@login_required(login_url='myapp:login')
def notify(request):
    context = {}
    dept = Department.objects.all()
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.From = request.user.userprofile.dept.dept_name
            obj.save()
            messages.success(request, 'Your message is sent successfully !')
            form = NotificationForm()
        else:
            messages.error(request, 'Please fill the correct detail!!')
    else:
        form = NotificationForm()
    context['form'] = form
    context['dept'] = dept
    return render(request, 'notify.html', context)


# Personal Notification
@login_required(login_url='myapp:login')
def personal(request):
    context = {}
    if request.method == 'POST':
        form = PersonalForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.From = request.user
            obj.save()
            messages.success(request, 'Your message is posted successfully!!')
            form = PersonalForm()
        else:
            messages.error(request, 'Please fill the correct details!!')
    else:
        form = PersonalForm()
    context['form'] = form
    return render(request, 'personal.html', context)


# Display Personal Notification
@login_required(login_url='myapp:login')
def personalshow(request):
    context = {}
    posts = sorted(Personalnote.objects.all(), key=attrgetter('Date'), reverse=True)
    pro = UserProfile.objects.get(id=request.user.userprofile.id)
    context['pro'] = pro

    # pagination
    page = request.GET.get('page', 1)
    posts_paginator = Paginator(posts, posts_per_page)
    try:
        posts = posts_paginator.page(page)
    except PageNotAnInteger:
        posts = posts_paginator.page(posts_per_page)
    except EmptyPage:
        posts = posts_paginator.page(posts_paginator.num_pages)

    context['posts'] = posts
    return render(request, 'personalshow.html', context)


# Apply Leave
@login_required(login_url='myapp:login')
def leave_apply(request):
    context = {}
    if request.method == 'POST':
        if request.user.is_authenticated:
            d = request.POST['date']
            d = datetime.datetime.strptime(d, '%Y-%m-%d').date()
            dt = datetime.date.today()
            if d < dt:
                form = LeaveApplyForm()
                context['form'] = form
                context['date_error'] = 'Please Choose Correct Date'
                return render(request, 'leave_apply.html', context)
            else:
                form = LeaveApplyForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    us = User.objects.get(pk=request.user.pk)
                    obj.user = us
                    obj.dept = request.user.userprofile.dept
                    obj.save()
                    messages.success(request, 'Your leave is sent successfully!!')

                    form = LeaveApplyForm()
        else:
            return render(request, 'login.html', {})
    else:
        form = LeaveApplyForm()
    context['form'] = form
    return render(request, 'leave_apply.html', context)


# Display pending leaves to manager of their relative department
@login_required(login_url='myapp:login')
def leave_view(request):
    context = {}
    if request.user.is_staff:
        leaves = LeaveApply.objects.all().filter(status=False, dept=request.user.userprofile.dept).order_by(
            '-date').exclude(
            user=request.user)
        page = request.GET.get('page', 1)
        posts_paginator = Paginator(leaves, posts_per_page)
        try:
            leaves = posts_paginator.page(page)
        except PageNotAnInteger:
            leaves = posts_paginator.page(posts_per_page)
        except EmptyPage:
            leaves = posts_paginator.page(posts_paginator.num_pages)

        context['leaves'] = leaves
        return render(request, 'leave-view.html', context)


# Leave is approved by manager and message is sent to employee
@login_required(login_url='myapp:login')
def approve_leave(request, pk):
    context = {}
    leave = LeaveApply.objects.filter(pk=pk).update(status=True)
    context['message'] = 'Leave Approved.'
    return render(request, 'approve-action.html', context)


# Leave is rejected by the manager and reply send on user's email
@login_required(login_url='myapp:login')
def reject_leave(request, pk):
    context = {}
    if request.method == 'POST':
        em = LeaveApply.objects.filter(pk=pk)
        for i in em:
            ema = i.user.email
        LeaveApply.objects.filter(pk=pk).delete()
        context['message'] = 'Leave Rejected.'
        message = 'Your Leave has been Rejected'
        mail_subject = 'Leave Status'
        to_email = ema
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
    return render(request, 'approve-action.html', context)


def error_404_view(request, exception):
    return render(request, '404.html', {'error': 404, 'er_txt': 'the page you are looking for not avaiable!'})


def error_500_view(request):
    return render(request, '500.html', {'error': 500, 'er_txt': 'Uh Oh!, Looks like server went way down hill'})
