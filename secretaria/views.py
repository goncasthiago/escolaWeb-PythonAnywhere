from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect,  get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from exercicios.models import Exercicios, ExercicioInstance, Materia, ExercicioInstance, Respostas
from secretaria.decorators import unauthenticated_user 
from users.models import User
from django.db.models import Q
import datetime
from django.forms.models import inlineformset_factory
import json
from .forms import ExerciciosForm, RespostasForm



class PadraoView(LoginRequiredMixin,View):
    login_url = 'accounts/login/'
    redirect_field_name = 'redirect_to'
    
    template_name = 'secretaria/home_aluno.html'
       
    
    def get(self, request, id=None, *args, **kwargs):
        if request.user.is_staff:
            self.template_name = 'secretaria/home_professor.html'

              
        user = User.objects.get(id=request.user.id)
        
        materias = Materia.objects.all()
        num_exercises = Exercicios.objects.all().count()
        #num_instances = ExercicioInstance.objects.filter(aluno=user).count()
        num_materias = Materia.objects.all().count()

        # Available exercises (status = 'a')
        num_instances_available = ExercicioInstance.objects.filter(aluno=user).filter(status__exact='n').count()
        num_instances_answered = ExercicioInstance.objects.filter(
           Q(aluno=user)).filter(Q(status__exact='a')).count()

        

        #metodo GET
        context = {
        'num_exercises': num_exercises,
        #'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_materias':num_materias,   
        'num_instances_answered': num_instances_answered,   
        'materias': materias,  
    }
    
        return render(request, self.template_name,context)

class CadastraExercicioView(LoginRequiredMixin,View):
    template_name = 'secretaria/cadastra_exercicios.html'
    context = {}

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('secretaria:inicial')
        prof = request.user
        form = ExerciciosForm(initial={'professor': prof})
        form_resposta_factory = inlineformset_factory(Exercicios, Respostas, form= RespostasForm, extra=4)
        form_resposta = form_resposta_factory()


        self.context = {
            'form': form,
            'form_resposta': form_resposta,
            
        }
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('secretaria:inicial')
        form = ExerciciosForm(request.POST)
        form_resposta_factory = inlineformset_factory(Exercicios, Respostas, form=RespostasForm)
        form_resposta = form_resposta_factory(request.POST)
        if form.is_valid() and form_resposta.is_valid():
            
            exercicio_novo = form.save(commit=False)
            exercicio_novo.professor = request.user
            exercicio_novo.pub_date = datetime.date.today()
            exercicio_novo.save()
            form_resposta.instance = exercicio_novo
            form_resposta.exercicio_id = exercicio_novo.id

            form_resposta.save()
            return redirect("secretaria:inicial")
        else:
            self.context = {
                'form': form,
                'form_resposta': form_resposta,
            }
        
        return render(request, self.template_name, self.context)

class DashboardView(LoginRequiredMixin,View):

    def statusResp( status ):
        resp = []
        for i in status:
            if i == 'a':
                resp.append('Acerto')
            elif i == 'e':
                resp.append('Erro')
            elif i == 'n':
                resp.append('Não Respondido')
            else:
                resp.append('Atrasado')
        return resp

    login_url = 'accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'secretaria/dashboard.html'

    queryset = ExercicioInstance.objects.order_by().values('status').annotate(quantidade=Count('status')).distinct()
    status = [obj['status'] for obj in queryset]
    quantidade = [obj['quantidade'] for obj in queryset]
    status = statusResp(status) 
    
    #status = map(statusResp, status) 

    context = {
        
       'status': json.dumps(status),
       'quantidade': json.dumps(quantidade),
    }

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('secretaria:inicial')

        return render(request, self.template_name, self.context)
