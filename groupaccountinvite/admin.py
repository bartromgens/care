from groupaccountinvite.models import GroupAccountInvite
#from accounts.models import Account
from django.contrib import admin

class GroupAccountInviteAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['groupAccount']}),
    (None, {'fields': ['inviter']}),
    (None, {'fields': ['invitee']}),
    (None, {'fields': ['isAccepted']}),
    (None, {'fields': ['isDeclined']}),]
  list_display = ('groupAccount', 'inviter', 'invitee', 'isAccepted', 'isDeclined')
    
#class AccountAdmin(admin.ModelAdmin):
    #fieldsets = [
        #(None, {'fields': ['name']}),
        #(None, {'fields': ['owner']}),
        #(None, {'fields': ['friends']}),
    #]
    #list_display = ('name', 'owner',)

admin.site.register(GroupAccountInvite, GroupAccountInviteAdmin)

#admin.site.register(Account, AccountAdmin)
