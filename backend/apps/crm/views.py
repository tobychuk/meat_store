from django.shortcuts import render
from django.views.generic import ListView, UpdateView, TemplateView, View
from backend.apps.crm.forms import DebtForm, ClientForm
from .models import Debt, Client
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
# Create your views here.
import datetime
import pandas as pd


def get_dates():
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=14)

    result = pd.date_range(
        min(start_date, end_date),
        max(start_date, end_date)
    ).strftime('%Y-%m-%d').tolist()
    return result

class IndexPage(ListView):
    model = Debt
    template_name = 'index.html'
    context_object_name = 'debts'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dates'] = get_dates()
        try:
            burning_debts = Debt.objects.filter(status='Не оплачен' or 'Частично оплачен').order_by('return_date')
        except:
            burning_debts = None
        context['burning_debts'] = burning_debts

        form = DebtForm()
        context['form'] = form
        context['this_date'] = datetime.datetime.today().strftime('%Y-%m-%d')
        context['is_index'] = True

        all_debts = Debt.objects.all()
        for debt in all_debts:
            if datetime.datetime.today().date() > debt.return_date:
                debt_upd = Debt.objects.filter(id=debt.id)
                debt_upd.update(status='Просрочен')
        return context

def get_date_page(request, date):
    try:
        debts = Debt.objects.filter(created=date)
    except Debt.DoesNotExist:
        raise Http404()

    try:
        burning_debts = Debt.objects.filter(status='Не оплачен' or 'Частично оплачен').order_by('return_date')
    except:
        burning_debts = None
    all_debts = Debt.objects.all()
    for debt in all_debts:
        if datetime.datetime.today().date() > debt.return_date:
            debt_upd = Debt.objects.filter(id=debt.id)
            debt_upd.update(status='Просрочен')
    if request.method == "POST":
        form = DebtForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect("index")
    else:
        form = DebtForm()
    context = {
        "debts":debts,
        "dates": get_dates(),
        "this_date":date,
        "burning_debts":burning_debts,
        "form":form
    }
    return render(request, 'index.html', context)

class UpdateDebtView(UpdateView):
    model = Debt
    form_class = DebtForm


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        global before_quantity
        before_quantity = self.object.quantity
        return super().post(request, *args, **kwargs)



    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


    def get_success_url(self):
        debt = Debt.objects.filter(id=self.object.id)
        if self.object.quantity <= 0:
            debt.update(status='Оплачен')
        elif self.object.quantity < before_quantity:
            debt.update(status='Частично оплачен')
        return reverse_lazy('datepage', args = [self.object.created])

class DebtsArchiveListView(ListView):
    model = Debt
    template_name = 'debts_archive_list.html'
    context_object_name = 'debts'

class ClientListView(ListView):
    model = Client
    template_name = 'client_list.html'
    context_object_name = 'clients'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        form = ClientForm()
        context['form'] = form
        return context

class AddClientView(View):
    def post(self, request):
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
        return redirect("clients_list")


class CalendarView(TemplateView):
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date = datetime.datetime(2022, 7, 1)
        end_date = datetime.datetime.today()
        dates = pd.date_range(
            min(start_date, end_date),
            max(start_date, end_date)
        ).strftime('%Y-%m-%d').tolist()
        context['dates'] = dates
        return context
