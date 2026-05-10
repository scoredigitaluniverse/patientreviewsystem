"""
URL configuration for review project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from reviewapp import views
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('login')),
    path('admin/', admin.site.urls),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('view_doctors/', views.view_doctors, name='view_doctors'),
    path('view_patients/', views.view_patients, name='view_patients'),
    path('doctor_dashboard/<int:doctor_id>/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient_details/<int:patient_id>/', views.patient_details, name='patient_details'),
    path('add_medical_history/<int:patient_id>/', views.add_medical_history, name='add_medical_history'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('add_review/', views.add_review, name='add_review'),
    path('view_reviews/', views.view_reviews, name='view_reviews'),
    
]
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)