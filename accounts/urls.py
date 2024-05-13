from django.urls import path
from accounts.views import option, logout, form_login, form_register, login, register

app_name = 'accounts'

urlpatterns = [
    path('', option, name='login'),
    path('login', form_login, name='form_login'),
    path('register', form_register, name='form_register'),
    path('logout', logout, name='logout'),
    path('log_in', login, name='log_in'),
    path('register/submit', register, name='register')
]
