from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name'
    ]

@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'debtor',
        'quantity'
    ]