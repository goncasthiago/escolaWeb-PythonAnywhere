
from django.shortcuts import render,redirect #, get_object_or_404
#from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Exercicios, ExercicioInstance, Materia, ExercicioInstance, Respostas
from users.models import User
from django.db.models import Q
from datetime import date


class PadraoView(LoginRequiredMixin,View):
    login_url = 'accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'exercicios/home.html'
    nome_materia = ""
    
    def get(self, request, id=None, *args, **kwargs):
        if self.nome_materia == "":
            materias = Materia.objects.all()
            
        else:
            materias = Materia.objects.get(name = self.nome_materia)

        user = User.objects.get(id=request.user.id)
        num_exercises = Exercicios.objects.all().count()
        num_instances = ExercicioInstance.objects.filter(aluno=user).count()
        num_materias = Materia.objects.all().count()
        #materias = Materia.objects.all()

        # Available exercises (status = 'a')
        num_instances_available = ExercicioInstance.objects.filter(aluno=user).filter(status__exact='n').count()
        num_instances_answered = ExercicioInstance.objects.filter(
           Q(aluno=user)).filter(Q(status__exact='a')).count()
        

        #metodo GET
        context = {
        'num_exercises': num_exercises,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_materias':num_materias,   
        'num_instances_answered': num_instances_answered,   
        'materias': materias,  
    }
    
        return render(request, self.template_name,context)

class ResumoExerciciosView(LoginRequiredMixin,View):
    login_url = 'accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'exercicios/exe.html'
    paginate_by = 10
    context = {}
    materias = Materia.objects.all()
    def get(self, request, id=None, *args, **kwargs):
        tasks = ExercicioInstance.objects.filter(aluno=self.request.user).filter(status__exact='n').order_by('until_date')
        latest_question_list = Exercicios.objects.order_by('pub_date')[:4]
        #output = ', '.join([q.enunciado for q in latest_question_list])
        
        self.context = {
            'latest_question_list' : latest_question_list,
            'tasks': tasks,
            'materias': self.materias,
        }
        
        return render(request, self.template_name,self.context)


class ExercicioInstanceByUserListView(LoginRequiredMixin,ListView):
    model = ExercicioInstance
    template_name ='exercicios/exe.html'
    paginate_by = 10

    def get_queryset(self):
        return ExercicioInstance.objects.filter(aluno=self.request.user).filter(status__exact='n').order_by('until_date')

class ExerciciosView(LoginRequiredMixin,View):
    login_url = 'accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'exercicios/questoes.html'
    materias = Materia.objects.all()
    context={}
    def get(self, request, id=None, *args, **kwargs):
        
        if id is not None:
            
           exercicio = Exercicios.objects.get(pk=id)
           alternativas = exercicio.respostas_set.all()
           self.context = {
            'questao' : exercicio,
            'alternativas': alternativas,
            'materias': self.materias

        }
                
        return render(request, self.template_name,self.context)
    def post(self, request, id=None, *args, **kwargs):
        resposta_correta = (request.POST['resposta']).split(sep="|")
        
        exercicio = Exercicios.objects.get(id=int(resposta_correta[0]))
        resposta = Respostas.objects.get(id=int(resposta_correta[1]))

        teste = ExercicioInstance.objects.filter(exercicio=exercicio).filter(aluno=request.user)[0]
        teste.answer_date = date.today()
        if resposta.is_correct:
            teste.status = 'a'
        else:
            teste.status = 'e'
        teste.alternativa = resposta
        teste.save()

            
        return redirect('exercicios:resumo')
