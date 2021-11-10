from django.contrib import admin

# Register your models here.
from .models import Materia, Exercicios, Respostas, ExercicioInstance

admin.site.register(Materia)
#admin.site.register(Exercicios)
##admin.site.register(Respostas)
#admin.site.register(ExercicioInstance)

class RespostaInline(admin.StackedInline):
    model = Respostas
    extra = 3

class ExInsInline(admin.TabularInline):
    model = ExercicioInstance

#@admin.register(Exercicios)
class ExerciciosAdmin(admin.ModelAdmin):
    list_display = ('enunciado', 'professor', 'materia')
    list_filter = ('materia', 'professor')

    inlines = [
        ExInsInline,
        ]

    fieldsets = [
        (None,               {'fields': ['enunciado', 'professor', 'materia']}),

        ('Date information', {'fields': ['pub_date','until_date'], 'classes': ['collapse']}),
    ]
    inlines = [RespostaInline]

admin.site.register(Exercicios, ExerciciosAdmin)



@admin.register(ExercicioInstance)
class ExercicioInstanceAdmin(admin.ModelAdmin):
    list_display = ('exercicio', 'status', 'aluno', 'id', 'answer_date', 'until_date')
    list_filter = ('status', 'answer_date', 'until_date')

    fieldsets = (
        (None, {
            'fields': ('aluno', 'id')
        }),
        ('Tarefas', {
            'fields': ('until_date', 'answer_date','exercicio','alternativa', 'status')
        }),
    )

