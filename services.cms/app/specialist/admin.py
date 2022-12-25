from django.contrib import admin
from specialist.models import DoctorSpecialist, Specialist

# Register your models here.
class DoctorSpecialistInline(admin.TabularInline):
    model = DoctorSpecialist
    
class SpecialistAdmin(admin.ModelAdmin):
    inlines = [
        DoctorSpecialistInline
    ]

class DoctorSpecialistAdmin(admin.ModelAdmin):
    pass


# admin.site.register(DoctorSpecialist, DoctorSpecialistAdmin)
admin.site.register(Specialist, SpecialistAdmin)