
from django.urls import path

from myapp import views

app_name = 'myapp'

urlpatterns = [
    path("", views.index, name='index'),
    path("login/", views.login, name='login'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("contact/", views.contact, name='contact'),
    path("devinfo/", views.devinfo, name='devinfo'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout, name='logout'),
    path('notify/', views.notify, name='notify'),
    path('personal/', views.personal, name='personal'),
    path('personalshow/', views.personalshow, name='personalshow'),
    path('leave_apply/', views.leave_apply, name='leave-apply'),
    path('leave_view', views.leave_view, name='view-leave'),
    path('view_leave', views.view_approve, name='view_approve'),
    path('approve/<pk>', views.approve_leave, name='approve'),
    path('reject/<pk>', views.reject_leave, name='rejected'),
]


