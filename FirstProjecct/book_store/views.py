from django.shortcuts import render
from django.http import HttpResponse
from .models import Student, HeadTeacher, FeeStructure, PaymentPlan, Payment
from django.views.generic import (CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView) # for class-based views
from django.urls import reverse_lazy 
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404


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

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-id')
        grade = self.kwargs.get('grade')
        if grade is not None:
            return Student.objects.filter(grade=grade).order_by('name')[:10]
        # Always limit to 10 students for display
        return Student.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Distinct grades for filter links
        context['grades'] = Student.objects.values_list('grade', flat=True).distinct().order_by('grade')
        context['selected_grade'] = self.kwargs.get('grade')
        context['total_students'] = Student.objects.count() 
        return context

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

# implementing CRUD operations for PaymentPlan and Payment models
#Payment plan is automatically created when a student is created, hence no need for a create view. plus there should be no manual adjustment of fees, hence no update view, left with list, and view.
class PaymentPlanListView(ListView):
    model = PaymentPlan
    template_name = 'students/payment_plan_list.html'
    context_object_name = 'payment_plans'  

class PaymentPlanDetailView(DetailView):
    model = PaymentPlan
    template_name = 'students/payment_plan_detail.html'  
    context_object_name = 'payment_plan'

class PaymentCreateView(CreateView):
    model = Payment
    fields = ['amount', 'description']
    template_name = 'students/payment_form.html'
    success_url = reverse_lazy('payment_plan_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs['student_id']
        context['student'] = get_object_or_404(Student, pk=student_id)
        return context

    def form_valid(self, form):
        # Get the student and their payment plan
        student_id = self.kwargs['student_id']
        student = get_object_or_404(Student, pk=student_id)
        form.instance.payment_plan = student.payment_plan

        # Save the payment and update the payment plan
        payment_plan = form.instance.payment_plan
        payment_plan.amount_paid += form.instance.amount
        payment_plan.save()

        return super().form_valid(form)
    
class PaymentListView(ListView):
    model = Payment
    template_name = 'payment_list.html'
    context_object_name = 'payments'

    def get_queryset(self):
        # Filter payments by a specific payment plan
        payment_plan_id = self.kwargs['payment_plan_id']
        return Payment.objects.filter(payment_plan_id=payment_plan_id)

class PaymentUpdateView(UpdateView):
    model = Payment
    fields = ['amount', 'description']
    template_name = 'payment_form.html'
    success_url = reverse_lazy('payment_plan_list')


class PaymentDeleteView(DeleteView):
    model = Payment
    template_name = 'payment_confirm_delete.html'
    success_url = reverse_lazy('payment_plan_list')