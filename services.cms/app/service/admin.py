# Register your models here.
from django.contrib import admin
from service.models import Service
# TabularInline - One to many relation
# Register your models here.

class ServiceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Service, ServiceAdmin)