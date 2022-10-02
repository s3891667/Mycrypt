from django.urls import path
from . import views
app_name = 'mycrypt'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.logIn, name='login'),
    path('logout/', views.logOut, name='logout'),
    path('signup/', views.signUp, name='signup'),
    path('forgot/', views.forgot, name='forgot'),
    path('home/', views.home, name='home'),
    path('learn/', views.learn, name='learn'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('coins/<str:coin_name>/', views.coins, name='coins'),
]
