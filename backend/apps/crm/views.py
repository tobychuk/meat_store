from django.shortcuts import render
from django.views.generic import ListView, UpdateView, TemplateView, View

from backend.apps.crm.forms import DebtForm, ClientForm

from .models import Debt, Client, Log
from .filters import DebtFilter
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
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
            burning_debts = Debt.objects.filter(status=Debt.STATUS_NOT_PAID).order_by('return_date')
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
                debt_upd = Debt.objects.filter(id=debt.id, status=Debt.STATUS_NOT_PAID)
                debt_upd.update(expired=True)
            else:
                debt_upd = Debt.objects.filter(id=debt.id, status=Debt.STATUS_NOT_PAID)
                debt_upd.update(expired=False)
        return context

def get_date_page(request, date):
    try:
        debts = Debt.objects.filter(created=date)
    except Debt.DoesNotExist:
        raise Http404()

    try:
        burning_debts = Debt.objects.filter(status=Debt.STATUS_NOT_PAID).order_by('return_date')
    except:
        burning_debts = None

    all_debts = Debt.objects.all()
    for debt in all_debts:
        if datetime.datetime.today().date() > debt.return_date:
            debt_upd = Debt.objects.filter(id=debt.id, status=Debt.STATUS_NOT_PAID)
            debt_upd.update(expired=True)
        else:
            debt_upd = Debt.objects.filter(id=debt.id, status=Debt.STATUS_NOT_PAID)
            debt_upd.update(expired=False)


    if request.method == "POST":
        form = DebtForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect("index")
    else:
        form = DebtForm()

    start_date = datetime.datetime.strptime(date, '%Y-%m-%d') - datetime.timedelta(days=7)
    end_date = datetime.datetime.strptime(date, '%Y-%m-%d') + datetime.timedelta(days=7)
    dates = pd.date_range(
        min(start_date, end_date),
        max(start_date, end_date)
    ).strftime('%Y-%m-%d').tolist()
    dates_list = dates[0:]

    for el_date in dates:
        if datetime.datetime.strptime(el_date, '%Y-%m-%d') > datetime.datetime.today():
            dates_list.remove(el_date)


    context = {
        "debts":debts,
        "dates": dates_list,
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

    def get_success_url(self):
        debt = Debt.objects.filter(id=self.object.id)
        if self.object.quantity <= 0:
            debt.update(status=Debt.STATUS_PAID)
        return reverse_lazy('datepage', args = [self.object.created])

    def form_valid(self, form):
        if form.changed_data:
            for field in form.changed_data:
                if field == 'quantity':
                    Log.objects.create(debt=self.get_object(), text=f'Размер долга изменился с {self.get_object().quantity} сом на {form.cleaned_data["quantity"]} сом')
                if field == 'amount_meat':
                    Log.objects.create(debt=self.get_object(), text=f'Количество мяса изменилось с {self.get_object().amount_meat} кг на {form.cleaned_data["amount_meat"]} кг')
                if field == 'created':
                    Log.objects.create(debt=self.get_object(), text=f'Дата выдачи изменилась с {self.get_object().created} на {form.cleaned_data["created"]}')
                if field == 'return_date':
                    Log.objects.create(debt=self.get_object(), text=f'Дата возврата изменилась с {self.get_object().return_date} на {form.cleaned_data["return_date"]}')
        return super().form_valid(form)

class UpdateClientDebtView(UpdateView):
    model = Debt
    form_class = DebtForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        global before_quantity
        before_quantity = self.object.quantity
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        debt = Debt.objects.filter(id=self.object.id)
        if self.object.quantity <= 0:
            debt.update(status=Debt.STATUS_PAID)
        return reverse_lazy('client_detail', args = [self.object.debtor.id])

    def form_valid(self, form):
        if form.changed_data:
            for field in form.changed_data:
                if field == 'quantity':
                    Log.objects.create(debt=self.get_object(), text=f'Размер долга изменился с {self.get_object().quantity} сом на {form.cleaned_data["quantity"]} сом')
                if field == 'amount_meat':
                    Log.objects.create(debt=self.get_object(), text=f'Количество мяса изменилось с {self.get_object().amount_meat} кг на {form.cleaned_data["amount_meat"]} кг')
                if field == 'created':
                    Log.objects.create(debt=self.get_object(), text=f'Дата выдачи изменилась с {self.get_object().created} на {form.cleaned_data["created"]}')
                if field == 'return_date':
                    Log.objects.create(debt=self.get_object(), text=f'Дата возврата изменилась с {self.get_object().return_date} на {form.cleaned_data["return_date"]}')
        return super().form_valid(form)


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
        debt_form = DebtForm()
        context['form'] = form
        context['debt_form'] = debt_form
        return context


class SearchClientListView(ListView):
    model = Client
    template_name = 'client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        search_text = self.request.GET.get('search')
        if search_text is None:
            return self.model.objects.all()
        q = self.model.objects.filter(
            Q(first_name__icontains=search_text)
            |Q(last_name__icontains=search_text)
        )
        return q

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        form = ClientForm()
        debt_form = DebtForm()
        context['form'] = form
        context['debt_form'] = debt_form
        context['search_query'] = self.request.GET.get('search')
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

    def post(self, request, *args, **kwargs):
        date = request.POST['date']
        return redirect('datepage', date)


class ClientDetailView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client_detail.html'
    context_object_name = 'client'

    def get_success_url(self):
        return reverse_lazy('client_detail', args=[self.object.id])


    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        status = self.request.GET.get('status')

        if not status:
            f = DebtFilter(self.request.GET, queryset=Debt.objects.filter(debtor=self.object.id))
        else:
            f = DebtFilter(self.request.GET, queryset=Debt.objects.filter(debtor=self.object.id,status=status))
            context['status'] = status

        context['filter'] = f

        return context
