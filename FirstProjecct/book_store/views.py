from django.shortcuts import render
from django.http import HttpResponse
from .models import Student, HeadTeacher, Fee
from django.views.generic import (CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView) # for class-based views
from django.urls import reverse_lazy 
from django.contrib import messages

# function-based view
def index(request):
    return HttpResponse("Welcome to my book store")

def student_list(request):
    students = Student.objects.all()
    return render(request, 'book_store/student_list.html', {'students': students}) # returning a dictionary of students to the template, still in the Django ORM

class StudentListView(TemplateView):
    template_name = 'hello.html' # in addition to the TemplateView which has been inherited, there are other generic views in Django that can be used to create views for your application. These include ListView, DetailView, CreateView, UpdateView, and DeleteView. With the use of these inheritance, we reduce the amount of codes we have to write.

#Task : using the generic views in the class-based views, practice relevant operations on the student model. Move to the urls.py to define the urls for the views.
class StudentCreateView(CreateView):
    model = Student
    fields = ['name', 'age', 'grade', 'guardian_name', 'guardian_address']
    template_name = 'students/student_form.html' 
    success_url = reverse_lazy('student_list')  

    def form_valid(self, form):
        try:
            latest_headteacher = HeadTeacher.objects.latest('id')
            form.instance.headteacher = latest_headteacher
            messages.success(self.request, f'Student assigned to {latest_headteacher.name}')
            return super().form_valid(form)
        except HeadTeacher.DoesNotExist:
            messages.error(self.request, 'No headteacher exist! Please create one first.')
            return self.form_invalid(form)
        
class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'  
    context_object_name = 'students'  
    #paginate_by = 10  # Number of items per page (optional)
    #ordering = ['name']  # Order by name (optional)
    def get_queryset(self):
        return Student.objects.select_related('fee', 'headteacher')
    
class StudentDetailView(DetailView):
    model = Student
    template_name = 'students/student_detail.html' 
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.object
        context['fee_amount'] = student.fee.amount if student.fee else None
        context['due_date'] = student.fee.due_date if student.fee else None
        return context  

class StudentUpdateView(UpdateView):
    model = Student
    fields = ['name', 'age', 'grade', 'guardian_name', 'guardian_address']
    template_name = 'students/student_form.html'  
    success_url = reverse_lazy('student_list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'  
    success_url = reverse_lazy('student_list')

class FeeCreateView(CreateView):
    model = Fee
    fields = '__all__'  
    template_name = 'students/fee_form.html'
    success_url = reverse_lazy('fee_list')

class FeeListView(ListView):
    model = Fee
    template_name = 'students/fee_list.html'  
    ordering = ['grade']

class FeeUpdateView(UpdateView):
    model = Fee
    fields = '__all__'  
    template_name = 'students/fee_form.html'  
    success_url = reverse_lazy('fee_list')