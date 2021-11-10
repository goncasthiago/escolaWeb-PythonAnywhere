import uuid # Required for unique exercises
from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from users.models import User
import datetime
from django.utils import timezone
from django.db.models.signals import post_save #, pre_save


class Materia(models.Model):
    """Modelo representando a materia do exercício."""
    name = models.CharField(max_length=200, help_text='Escreva o nome da matéria')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Exercicios(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    enunciado = models.CharField(max_length=500)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    professor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    pub_date = models.DateTimeField('date published',null=True, blank=True)
    is_active = models.BooleanField(default=True)
    until_date = models.DateTimeField(null=True, blank=True)
    #until_date = models.DateTimeField('date published', help_text='Até quando esse exercício deverá ser entregue')

        # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    #materia = models.ManyToManyField(Materia, help_text='Selecione a materia desse exercício')
    materia = models.ForeignKey('Materia', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.enunciado

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=30)
    
    def get_answer(self):
        return self.respostas_set.all()
    
    @property
    def active(self):
        if self.until_date and datetime.date.today() > self.until_date:
            return False
        return True
        
    #def display_materia(self):
    #    """Create a string for the Materia. This is required to display materia in Admin."""
    #    return ', '.join(materia.name for materia in self.materia.all()[:3])

    #display_materia.short_description = 'Materia'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this exercise."""
        return reverse('exercicio-detail', args=[str(self.id)])







class Respostas(models.Model):
    exercicio = models.ForeignKey(Exercicios, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    resposta_texto = models.CharField(max_length=200)
    def __str__(self):
        """String for representing the Model object."""
        return self.resposta_texto
    

class ExercicioInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='ID unico desse exercício')
    exercicio = models.ForeignKey('Exercicios', on_delete=models.RESTRICT, null=True)
    until_date = models.DateField(null=True, blank=True)
    aluno = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    alternativa = models.ForeignKey('Respostas', on_delete=models.RESTRICT, null=True)
    answer_date = models.DateField(null=True, blank=True) 
    acertou = models.BooleanField(null=True)

    LOAN_STATUS = (
        ('a', 'Acerto'),
        ('e', 'Erro'),
        ('n', 'Não Respondido'),
        ('t', 'Atrasado'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='n',
        help_text='Status do exercício',
    )

    class Meta:
        ordering = ['until_date']

    def __str__(self):
        """String for representing the Model object."""
        return self.exercicio.enunciado
    
    @property
    def is_late(self):
        if self.until_date and datetime.date.today() > self.until_date:
            return True
        return False
    
def save_post(sender, instance, **kwargs):
    
    alunos = User.objects.all()
    for atual in alunos:
        exercicio_novo = ExercicioInstance()
        exercicio_novo.exercicio = instance
        exercicio_novo.until_date = instance.until_date
        exercicio_novo.aluno = atual
        exercicio_novo.status = 'n'
        exercicio_novo.save()

     
post_save.connect(save_post, sender=Exercicios)