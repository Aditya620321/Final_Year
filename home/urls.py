from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
app_name = 'home'


def home_view(request):
    return render(request, 'home/home.html')

urlpatterns = [
    path('', views.home_view, name='home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
