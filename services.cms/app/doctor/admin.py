from django.contrib import admin
from doctor.models import Doctor, Specification, WorkingShift, Package
from specialist.admin import DoctorSpecialistInline
# TabularInline - One to many relation
# Register your models here.

class SpecsInline(admin.TabularInline):
    model = Specification
    
class ShiftInline(admin.TabularInline):
    model = WorkingShift
    
class PackageInline(admin.TabularInline):
    model = Package
class DoctorAdmin(admin.ModelAdmin):
    inlines = [
        SpecsInline,
        ShiftInline,
        PackageInline,
        DoctorSpecialistInline
    ]

class SpecificationAdmin(admin.ModelAdmin):
    pass

class ShiftAdmin(admin.ModelAdmin):
    pass

class PackageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Specification, SpecificationAdmin)
admin.site.register(WorkingShift, ShiftAdmin)
admin.site.register(Package, PackageAdmin)
