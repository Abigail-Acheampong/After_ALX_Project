"""
URL configuration for FirstProjecct project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from book_store.views import SignUpView

urlpatterns = [
    path('books/', include('book_store.urls')),    
    path('admin/', admin.site.urls),

    # important to keep these urls here because:
    # authentication affect the whole project not just the app
    # the first url is part of Django's built-in authentication system
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', TemplateView.as_view(template_name='accounts/profile.html'),
             name='profile'),
    path("signup/", SignUpView.as_view(), name="templates/registration/signup"),

]
