from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from data.models import CustomerProfile


# Create your views here.
class HomeView(LoginRequiredMixin,ListView):
    template_name = 'home2.html'
    login_url = '/admin'
    
    # def get(self, request, *args, **kwargs):
    #     context = self.get_context_data(**kwargs)
    #     # context['test'] = {'test':'Hello World'}
    #     return self.render_to_response(context)

    model = CustomerProfile
    context_object_name = 'customers'


class DetailView(LoginRequiredMixin,DetailView):
    template_name = 'detail.html'
    login_url = '/admin'
    model = CustomerProfile
    context_object_name = 'customer'