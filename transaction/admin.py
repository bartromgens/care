from django.contrib import admin

from transaction.models import Transaction
from transaction.models import Modification


class TransactionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['what']}),
        (None, {'fields': ['date']}),
        (None, {'fields': ['amount']}),
        (None, {'fields': ['groupAccount']}),
        (None, {'fields': ['buyer']}),
        (None, {'fields': ['consumers']}), ]
    list_display = ('what', 'amount', 'groupAccount', 'buyer', 'date')
    list_filter = ['date']
    search_fields = ['what']
    date_hierarchy = 'date'

admin.site.register(Transaction, TransactionAdmin)


class ModificationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['date']}),
        (None, {'fields': ['user']}), ]
    list_display = ('date', 'user')

admin.site.register(Modification, ModificationAdmin)
