from django.shortcuts import render
from django.views.generic import ListView, View
from .models import Debt
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
import datetime
import pandas as pd

def get_dates():
    start_date = datetime.datetime(2022, 7, 1)
    print(start_date)
    end_date = datetime.datetime.today()
    print(end_date)

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
        return context

def get_date_page(request, date):
    try:
        debts = Debt.objects.filter(created=date)
    except Debt.DoesNotExist:
        raise Http404()

    try:
        burning_debts = Debt.objects.order_by('return_date')
    except:
        burning_debts = None
    context = {
        "debts":debts,
        "dates": get_dates(),
        "this_date":date,
        "burning_debts":burning_debts
    }
    return render(request, 'index.html', context)

