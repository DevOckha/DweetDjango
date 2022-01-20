from django.urls import path
from .views import dashboard, profile_list, profile, registerPage, loginPage, logoutUser

app_name = 'dwitter'

urlpatterns = [
    path('', registerPage, name='register'),
    path('login/', loginPage, name="login"),  
    path('logout/', logoutUser, name="logout"),

    path('dashboard/', dashboard, name='dashboard'),
    path('profile_list/', profile_list, name='profile_list'),
    path('profile/<int:pk>/', profile, name='profile'),
]


