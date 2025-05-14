from django.urls import path
from accounts.views import activate_email
from . import views

urlpatterns = [
   path('activate/<email_token>/' , activate_email , name="activate_email"),
   #login and register
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]
