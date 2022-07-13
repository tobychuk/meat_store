from django.urls import path, include
from .views import IndexPage
urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
]