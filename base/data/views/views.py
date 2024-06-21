from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from data.models import CustomerProfile, CustomerLedger, BalanceChange

class HomeView(LoginRequiredMixin, ListView):
    template_name = 'home.html'
    login_url = '/admin'
    model = CustomerProfile
    context_object_name = 'customers'

class DetailView(LoginRequiredMixin, DetailView):
    template_name = 'detail.html'
    login_url = '/admin'
    model = CustomerProfile
    context_object_name = 'customer'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = CustomerProfile.objects.all()
        try:
            context['ledger'] = CustomerLedger.objects.get(customer=context['customer'])
        except CustomerLedger.DoesNotExist:
            context['ledger'] = None
        
        # Fetch and limit balance change records related to the customer to 10 most recent
        context['balance_changes'] = BalanceChange.objects.filter(receiver=context['customer']).order_by('-transaction_date')[:10]
        
        return context
