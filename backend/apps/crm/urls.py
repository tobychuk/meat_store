from django.urls import path, include
from .views import IndexPage, get_date_page
urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('date/<str:date>/', get_date_page, name='datepage')
]