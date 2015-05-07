from django.contrib import admin

from transaction.models import Transaction
from transaction.models import TransactionReal
from transaction.models import Modification


class TransactionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['what']}),
        (None, {'fields': ['date']}),
        (None, {'fields': ['amount']}),
        (None, {'fields': ['group_account']}),
        (None, {'fields': ['buyer']}),
        (None, {'fields': ['consumers']}), ]
    list_display = ('what', 'amount', 'group_account', 'buyer', 'date')
    list_filter = ['date']
    search_fields = ['what']
    date_hierarchy = 'date'

admin.site.register(Transaction, TransactionAdmin)


class TransactionRealAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['amount']}),
        (None, {'fields': ['sender']}),
        (None, {'fields': ['receiver']}),
        (None, {'fields': ['comment']}),
        (None, {'fields': ['group_account']}), ]
    list_display = ('amount', 'sender', 'receiver', 'group_account', 'comment', 'date')
    list_filter = ['date']
    search_fields = ['what']
    date_hierarchy = 'date'

admin.site.register(TransactionReal, TransactionRealAdmin)


class ModificationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['date']}),
        (None, {'fields': ['user']}), ]
    list_display = ('date', 'user')

admin.site.register(Modification, ModificationAdmin)
