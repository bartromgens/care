from django.contrib import admin

from transactionreal.models import TransactionReal

class TransactionRealAdmin(admin.ModelAdmin):
    fieldsets = [
      (None, {'fields': ['amount']}),
      (None, {'fields': ['sender']}),
      (None, {'fields': ['receiver']}),
      (None, {'fields': ['comment']}),
      (None, {'fields': ['groupAccount']}),]
    list_display = ('amount', 'sender', 'receiver', 'groupAccount', 'comment', 'date')
    list_filter = ['date']
    search_fields = ['what']
    date_hierarchy = 'date'

admin.site.register(TransactionReal, TransactionRealAdmin)

#admin.site.register(Account, AccountAdmin)
