from django.contrib import admin

# Register your models here.
from .models import Student, HeadTeacher

# customizing the admin interface for the Student model
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'grade', 'guardian_name', 'guardian_address', 'headteacher')
    search_fields = ('name', 'guardian_name')
    list_filter = ('grade', 'headteacher')

class HeadTeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'qualification', 'date_appointed')
    search_fields = ('name',)
    list_filter = ('date_appointed',)

# Register the Student model with the admin site
admin.site.register(Student, StudentAdmin)
admin.site.register(HeadTeacher, HeadTeacherAdmin)
# This will allow you to manage Student records through the Django admin interface.



