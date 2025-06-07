from django.urls import path, include
from .import views
from .views import (StudentListView,StudentCreateView,StudentDetailView,StudentUpdateView,StudentDeleteView,
FeeStructureCreateView, FeeStructureListView, FeeStructureUpdateView, FeeStructureDeleteView, 
PaymentPlanListView, PaymentPlanDetailView, 
    PaymentCreateView, PaymentListView, PaymentUpdateView, PaymentDeleteView, PaymentReceiptView, PaymentReceiptPDFView, generate_pdf, download_class_list_pdf) 

urlpatterns = [
    # FeeStructure URLs
    path('fee-structures/', FeeStructureListView.as_view(), name='fee_structure_list'),
    path('fee-structures/create/', FeeStructureCreateView.as_view(), name='fee_structure_create'),
    path('fee-structures/<int:pk>/update/', FeeStructureUpdateView.as_view(), name='fee_structure_update'),
    path('fee-structures/<int:pk>/delete/', FeeStructureDeleteView.as_view(), name='fee_structure_delete'),
    
    # path('', views.index, name='index'),
    path('', StudentListView.as_view(), name='student_list'),
    path('grade/<int:grade>/', StudentListView.as_view(), name='student_list_by_grade'),
    path('create/', StudentCreateView.as_view(), name='student_create'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('<int:pk>/update/', StudentUpdateView.as_view(), name='student_update'),
    path('<int:pk>/delete/', StudentDeleteView.as_view(), name='student_delete'),

 # PaymentPlan URLs
    path('payment-plans/', PaymentPlanListView.as_view(), name='payment_plan_list'),
    path('payment-plans/<int:pk>/', PaymentPlanDetailView.as_view(), name='payment_plan_detail'),

    # Payment URLs
    path('payments/create/<int:student_id>/', PaymentCreateView.as_view(), name='payment_create'),
    path('payments/<int:payment_plan_id>/', PaymentListView.as_view(), name='payment_list'),
    path('payments/<int:pk>/update/', PaymentUpdateView.as_view(), name='payment_update'),
    path('payments/<int:pk>/delete/', PaymentDeleteView.as_view(), name='payment_delete'),
    path('payments/receipt/<int:pk>/', PaymentReceiptView.as_view(), name='payment_receipt'),
    path('payments/receipt/<int:pk>/download/', PaymentReceiptPDFView.as_view(), name='download_receipt'),

      path('students/pdf-report/', generate_pdf, name='generate_pdf'),
    
    path('grades/<int:grade>/download/', download_class_list_pdf, name='download_class_list_pdf'),

]