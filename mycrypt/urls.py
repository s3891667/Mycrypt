from django.urls import path
from django.conf.urls import url
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
    path('post/', views.post, name='post'),
    path('remove/', views.remove, name='remove'),
    path('coins/<str:coin_name>/', views.coins, name='coins'),
    path('reset/', views.resetPass, name='reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/',
        views.link, name='link'),
]
