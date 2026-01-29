from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('upload/', views.upload_view, name='upload'),
    path('login/', views.login_view, name='login'),
    path('check-result/', views.check_result, name='check_result'),
    path('logout/', views.logout_view, name='logout'),
]