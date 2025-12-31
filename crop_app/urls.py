from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detect/', views.detect_disease, name='detect_disease'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('get-weather/', views.get_weather, name='get_weather'),
    path('faq/', views.faq_page, name='faq')


]
