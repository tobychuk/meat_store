from django import forms
from backend.apps.crm.models import Debt
from django_filters import FilterSet, ChoiceFilter

class DebtFilter(FilterSet):
    status = ChoiceFilter(choices=Debt.DEBT_STATUSES)
    class Meta:
        model = Debt
        fields = [
            'status',
            ]