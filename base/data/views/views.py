from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class HomeView(LoginRequiredMixin,TemplateView):
    template_name = 'home.html'
    login_url = '/admin'
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['test'] = {'test':'Hello World'}
        return self.render_to_response(context)
