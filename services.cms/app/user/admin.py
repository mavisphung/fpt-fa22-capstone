from django.contrib import admin
from user.models import User, Notification

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass

class NotificationAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Notification, NotificationAdmin)