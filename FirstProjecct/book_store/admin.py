from django.contrib import admin

# Register your models here.
from .models import Student

# customizing the admin interface for the Student model
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'grade', 'guardian_name', 'guardian_address')
    search_fields = ('name', 'guardian_name')
    list_filter = ('grade',)

# Register the Student model with the admin site
admin.site.register(Student, StudentAdmin)
# This will allow you to manage Student records through the Django admin interface.



