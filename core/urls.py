# core/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('guest/', views.guest, name='guest'),
    path('cesostaff/dashboard/', views.cesostaff_dashboard, name='cesostaff_dashboard'),
    path('create-activity/', views.create_activity, name='create_activity'),
    path('manage-activities/', views.manage_activities, name='manage_activities'),
    path('manage-research/', views.manage_research, name='manage_research'),
    path('manage-certificates/', views.manage_certificates, name='manage_certificates'),
    path('view-reports/', views.view_reports, name='view_reports'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('activities/<int:pk>/', views.view_activity, name='view_activity'),
    path('activities/<int:pk>/update/', views.update_activity, name='update_activity'),
]

