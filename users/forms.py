from django import forms
from .models import User

class FormUser(forms.ModelForm):
    name = forms.CharField( label='', widget=forms.TextInput(
       attrs={
            "class" : "input is-normal is-hovered",
            "placeholder" : "Nome do Aluno",
        }
    ))
    
    email = forms.EmailField(
        label='', widget=forms.TextInput(
       attrs={
            "class" : "input is-normal is-hovered",
            "placeholder" : "E-mail de contato",
        }
    )
    )



    class Meta:
        model = User
        fields = [ 
            'nome',
            'email',
         ]
    
    #Faz o teste no campo email
    #def clean_email(self, *args, **kwargs):
    #    email = self.cleaned_data.get('email')
    #    if not "@gmail" in email:
    #        raise forms.ValidationError("Necessário cadastrar um e-mail do Gmail!")
    #    return email
            
    def clean_name(self, *args, **kwargs):
            name = self.cleaned_data.get('name')
            if name is "":
                raise forms.ValidationError("Necessário cadastrar um nome!")
            return name