from groupaccount.models import GroupAccount
#from accounts.models import Account
from django.contrib import admin

class GroupAccountAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['number']}),
        (None, {'fields': ['name']}),
    ]
    
#class AccountAdmin(admin.ModelAdmin):
    #fieldsets = [
        #(None, {'fields': ['name']}),
        #(None, {'fields': ['owner']}),
        #(None, {'fields': ['friends']}),
    #]
    #list_display = ('name', 'owner',)

admin.site.register(GroupAccount, GroupAccountAdmin)

#admin.site.register(Account, AccountAdmin)
