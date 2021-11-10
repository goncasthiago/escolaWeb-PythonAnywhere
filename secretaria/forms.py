from django import forms
from exercicios.models import Exercicios, Respostas, Materia

materias = Materia.objects.all()
materias_ids = [materia.id for materia in materias]
materia_set = Materia.objects.filter(id__in=materias_ids)

class ExerciciosForm(forms.ModelForm):
    enunciado = forms.CharField( label='Enunciado', max_length=400, widget=forms.Textarea(
       attrs={
            "class" : "input is-normal is-hovered",
            
        }
    ))
    #materia = forms.ChoiceField(
    #    #required=True,
    #    widget=forms.Select,
    #    choices= Materia.objects.values_list()
    #)
    materia = forms.ModelChoiceField(queryset= materia_set, required=True)

    
    is_active = forms.BooleanField(label="Pergunta ativa", initial=True )
    until_date = forms.DateField(label="Entregar até")
    
    class Meta:
        model = Exercicios
        fields = [
            'enunciado', 
            'is_active', 
            'until_date', 
            'materia',
            #'professor'
            ]

class RespostasForm(forms.ModelForm):
    resposta_texto = forms.CharField( label='Resposta', max_length=400, widget=forms.Textarea(
       attrs={
            "class" : "input is-normal is-hovered",
            
        }
    ))
    is_correct = forms.BooleanField(label="Alternativa correta", required=False)
    class Meta:
        model = Respostas
        fields = [
            'resposta_texto',
             'is_correct',
        ]
        