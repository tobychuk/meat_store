from django.urls import path, include
from .views import *
urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('debts_list/<str:date>/', get_date_page, name='datepage'),
    path('archive/debts_list/', DebtsArchiveListView.as_view(), name='debt_archive'),
    path('debt/update/<int:pk>', UpdateDebtView.as_view(), name='debt_update'),
    path('clients/list', ClientListView.as_view(), name='clients_list'),
    path('client/add', AddClientView.as_view(), name='add_client'),
    path('debts_calendar/', CalendarView.as_view(), name='calendar'),
    path('client/detail/<int:pk>', ClientDetailView.as_view(), name='client_detail')
]