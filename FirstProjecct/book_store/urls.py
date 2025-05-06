from django.urls import path 
from .import views
from .views import (StudentListView,StudentCreateView,StudentDetailView,StudentUpdateView,StudentDeleteView,
FeeStructureCreateView, FeeStructureListView, FeeStructureUpdateView, FeeStructureDeleteView,)

urlpatterns = [
    # FeeStructure URLs
    path('fee-structures/', FeeStructureListView.as_view(), name='fee_structure_list'),
    path('fee-structures/create/', FeeStructureCreateView.as_view(), name='fee_structure_create'),
    path('fee-structures/<int:pk>/update/', FeeStructureUpdateView.as_view(), name='fee_structure_update'),
    path('fee-structures/<int:pk>/delete/', FeeStructureDeleteView.as_view(), name='fee_structure_delete'),
    
    # path('', views.index, name='index'),
    path('', StudentListView.as_view(), name='student_list'),
    path('create/', StudentCreateView.as_view(), name='student_create'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('<int:pk>/update/', StudentUpdateView.as_view(), name='student_update'),
    path('<int:pk>/delete/', StudentDeleteView.as_view(), name='student_delete')
]