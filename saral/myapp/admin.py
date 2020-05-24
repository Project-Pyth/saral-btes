from django.contrib import admin
from myapp.models import UserProfile, Department, Notification, Personalnote, Attendance, LeaveApply, Subjects


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['From', 'Subject', 'Date', 'status', ]


class PersonalnoteAdmin(admin.ModelAdmin):
    list_display = ['From', 'Sub', 'Date', ]


class LeaveApplyAdmin(admin.ModelAdmin):
    list_display = ['user', 'dept', 'reason', 'date', 'status', ]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'dept', 'designation', ]

    def get_queryset(self, request):
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        queryset = queryset.order_by('user', )
        return queryset


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Department)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Personalnote, PersonalnoteAdmin)
admin.site.register(Attendance)
admin.site.register(LeaveApply, LeaveApplyAdmin)
admin.site.register(Subjects)

admin.site.site_header = 'Saral Admin'
admin.site.site_title = 'Saral'
