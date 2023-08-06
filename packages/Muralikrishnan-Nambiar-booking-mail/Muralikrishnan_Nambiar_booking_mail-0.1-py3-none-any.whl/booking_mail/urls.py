from django.urls import path
from . import views

app_name = 'booking_mail'

urlpatterns = [
    path('generate/<str:email>/', views.send_email, name='send_email'),
]