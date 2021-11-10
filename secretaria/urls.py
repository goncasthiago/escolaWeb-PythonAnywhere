from django.urls import path
from .views import PadraoView,CadastraExercicioView, DashboardView


app_name = 'secretaria'

urlpatterns = [
    path('', PadraoView.as_view(), name='inicial'),
    path('novas-questoes/',CadastraExercicioView.as_view(), name='cadastra'),
    path('dashboard/',DashboardView.as_view(), name='dashboard'),
   # path('exercicios/', PadraoView.as_view(template_name = 'secretaria/exercicios.html'), name='exercicios'),
]