from django.urls import path
from accounts.views import form_login, form_register, login

app_name = 'accounts'

urlpatterns = [
    path('', login, name='login'),
    path('login', form_login, name='form_login'),
    path('register', form_register, name='form_register'),
]