from django.urls import path
from .views import PadraoView, ExerciciosView, ResumoExerciciosView, ExercicioInstanceByUserListView

app_name='exercicios'

urlpatterns = [
    path('', PadraoView.as_view(), name='inicial'),
    path('questoes/',ResumoExerciciosView.as_view(), name='resumo'),
    #path('questoes/',ExercicioInstanceByUserListView.as_view(), name='resumo'),
    path('questoes/<int:id>', ExerciciosView.as_view(), name='questoes'),
]