from django.shortcuts import render
from django.http import HttpResponse
from .models import Student, HeadTeacher, FeeStructure 
from django.views.generic import (CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView) # for class-based views
from django.urls import reverse_lazy 
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


# function-based view
def index(request):
    return HttpResponse("Welcome to my book store")

def student_list(request):
    students = Student.objects.all()
    return render(request, 'book_store/student_list.html', {'students': students}) # returning a dictionary of students to the template, still in the Django ORM

class StudentListView(TemplateView):
    template_name = 'hello.html' # in addition to the TemplateView which has been inherited, there are other generic views in Django that can be used to create views for your application. These include ListView, DetailView, CreateView, UpdateView, and DeleteView. With the use of these inheritance, we reduce the amount of codes we have to write.

#Task : using the generic views in the class-based views, practice relevant operations on the student model. Move to the urls.py to define the urls for the views.
# FeeStructure Views
class FeeStructureCreateView(CreateView):
    model = FeeStructure
    fields = ['grade', 'amount', 'description', 'effective_from', 'active']
    template_name = 'students/fee_structure_form.html'
    success_url = reverse_lazy('fee_structure_list')

class FeeStructureListView(ListView):
    model = FeeStructure
    template_name = 'students/fee_structure_list.html'
    context_object_name = 'fee_structures'

class FeeStructureUpdateView(UpdateView):
    model = FeeStructure
    fields = ['grade', 'amount', 'description', 'effective_from', 'active']
    template_name = 'students/fee_structure_form.html'
    success_url = reverse_lazy('fee_structure_list')

class FeeStructureDeleteView(DeleteView):
    model = FeeStructure
    template_name = 'students/fee_structure_confirm_delete.html'
    success_url = reverse_lazy('fee_structure_list')

class StudentCreateView(CreateView):
    model = Student
    fields = ['name', 'age', 'grade', 'guardian_name', 'guardian_address']
    template_name = 'students/student_form.html' 
    success_url = reverse_lazy('student_list')  

    def form_valid(self, form):
        try:
            # Automatically assign the latest headteacher
            latest_headteacher = HeadTeacher.objects.latest('id')
            form.instance.headteacher = latest_headteacher

            # Automatically assign the fee structure based on the student's grade
            fee_structure = FeeStructure.objects.filter(grade=form.instance.grade).first()
            if fee_structure:
                form.instance.fee_structure = fee_structure
                messages.success(self.request, f'Student assigned to {latest_headteacher.name} and Fee Structure for Grade {fee_structure.grade}')
            else:
                messages.warning(self.request, f'No Fee Structure found for Grade {form.instance.grade}. Please create one.')

            return super().form_valid(form)
        except HeadTeacher.DoesNotExist:
            messages.error(self.request, 'No headteacher exists! Please create one first.')
        
class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'  
    context_object_name = 'students'  
    #paginate_by = 10  # Number of items per page (optional)
    #ordering = ['name']  # Order by name (optional)

class StudentDetailView(DetailView):
    model = Student
    template_name = 'students/student_detail.html' 
    context_object_name = 'student'  

class StudentUpdateView(UpdateView):
    model = Student
    fields = ['name', 'age', 'grade', 'guardian_name', 'guardian_address']
    template_name = 'students/student_form.html'  
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        # Automatically update the fee structure based on the updated grade
        fee_structure = FeeStructure.objects.filter(grade=form.instance.grade).first()
        if fee_structure:
            form.instance.fee_structure = fee_structure
            messages.success(self.request, f'Fee Structure for Grade {fee_structure.grade} assigned.')
        else:
            messages.warning(self.request, f'No Fee Structure found for Grade {form.instance.grade}. Please create one.')
        return super().form_valid(form)

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'  
    success_url = reverse_lazy('student_list')

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"