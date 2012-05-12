from django.contrib import admin

from transaction.models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['what']}),
        (None, {'fields': ['amount']}),
        (None, {'fields': ['groupAccount']}),
        (None, {'fields': ['date']}),
        (None, {'fields': ['buyer']}),
        (None, {'fields': ['consumers']}),
    ]
    list_display = ('what', 'amount', 'groupAccount', 'buyer', 'date')
    list_filter = ['date']
    search_fields = ['what']
    date_hierarchy = 'date'

admin.site.register(Transaction, TransactionAdmin)

#admin.site.register(Account, AccountAdmin)
