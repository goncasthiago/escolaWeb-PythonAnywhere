from django.urls import path
from .views import PadraoView

app_name = 'users'

urlpatterns = [
    path('', PadraoView.as_view(), name='perfil'),
    
]