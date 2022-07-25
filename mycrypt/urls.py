from django.urls import path

from . import views
app_name = 'mycrypt'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.logIn, name='login'),
    path('logout/', views.logOut, name='logout'),
    path('signup/', views.signUp, name='signup')

]
