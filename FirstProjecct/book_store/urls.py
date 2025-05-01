from django.urls import path 
from .import views
from .views import (StudentListView,StudentCreateView,StudentDetailView,StudentUpdateView,StudentDeleteView, FeeListView, FeeCreateView, FeeUpdateView)

urlpatterns = [
    # path('', views.index, name='index'),
    path('', StudentListView.as_view(), name='student_list'),
    path('create/', StudentCreateView.as_view(), name='student_create'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('<int:pk>/update/', StudentUpdateView.as_view(), name='student_update'),
    path('<int:pk>/delete/', StudentDeleteView.as_view(), name='student_delete'),
    path('fees/', FeeListView.as_view(), name='fee_list'),
    path('fees/create/', FeeCreateView.as_view(), name='fee_create'),
    path('fees/<int:pk>/update/', FeeUpdateView.as_view(), name='fee_update'),
]