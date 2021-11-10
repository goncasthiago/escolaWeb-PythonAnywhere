from django.shortcuts import render, get_object_or_404
from django.views import View
from users.models import User

class PadraoView(View):
    template_name = 'users/profile.html'
    context = {}
    def get(self, request, id=None, *args, **kwargs):
        id = request.user.id
        if id is not None:
            obj = get_object_or_404(User, id=id)
            self.context['object'] = obj
        for item in self.context:
            print(item)
    
        return render(request, self.template_name,self.context)