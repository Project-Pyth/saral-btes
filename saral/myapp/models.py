from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator  # Validation for Phone number
from datetime import date
from django.utils.timezone import now

from django.utils import timezone

DESG = (
    ('Manager', 'Manager'),
    ('Employee', 'Employee')
)


# Department Detail

class Department(models.Model):
    dept_name = models.CharField(max_length=30, unique=True, blank=False)

    def __str__(self):
        return self.dept_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links With User Model
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, default=None, blank=True, null=True)
    designation = models.CharField(max_length=15, choices=DESG)
    ph = RegexValidator(regex=r'^\+?1?\d{10,10}$', message="Enter in format +9999999999. Upto 10 digits allowed")
    contact = models.CharField(validators=[ph], max_length=11, blank=False)
    address = models.CharField(max_length=100, blank=False)
    image = models.ImageField(upload_to='profile_image', blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except ObjectDoesNotExist:
        UserProfile.objects.create(user=instance)


# Official Notification

class Notification(models.Model):
    To = models.ForeignKey(Department, on_delete=models.CASCADE)
    From = models.CharField(max_length=30, blank=False, default=None)
    Subject = models.CharField(max_length=100, blank=False)
    Content = models.TextField(max_length=700, blank=False)
    Date = models.DateTimeField(default=now)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.Subject


# Personal Notifications Subject
class Subjects(models.Model):
    sub = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.sub

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"


# Personal Notification
class Personalnote(models.Model):
    From = models.ForeignKey(User, on_delete=models.CASCADE)
    Sub = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    Content = models.TextField(max_length=700, blank=False)
    Date = models.DateTimeField(default=now)

    def __str__(self):
        return self.Sub


# Attendance table
class Attendance(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    Month = models.DateTimeField()
    Work_Day = models.IntegerField()
    Leave = models.IntegerField()
    Dayoff = models.IntegerField()

    def __str__(self):
        return self.Month


# Leave Apply
class LeaveApply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, default=None, blank=True, null=True)
    status = models.BooleanField(default=False)
    days_asked = models.PositiveIntegerField(default=2)
    days_approved = models.PositiveIntegerField(default=1)
    date = models.DateField(default=now)
    reason = models.TextField(max_length=2000)

    class Meta:
        verbose_name = 'Leave Application'
        verbose_name_plural = 'Leave Applications'

    def __str__(self):
        return 'Leave by ' + self.user.username + ' for the reason ' + self.reason[0:20]
