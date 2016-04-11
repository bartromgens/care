from django.contrib import admin

from care.groupaccountinvite.models import GroupAccountInvite
#from accounts.models import Account


class GroupAccountInviteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['group_account']}),
        (None, {'fields': ['inviter']}),
        (None, {'fields': ['invitee']}),
        (None, {'fields': ['isAccepted']}),
        (None, {'fields': ['isDeclined']}), ]
    list_display = ('group_account', 'inviter', 'invitee', 'isAccepted', 'isDeclined')

#class AccountAdmin(admin.ModelAdmin):
      #fieldsets = [
          #(None, {'fields': ['name']}),
          #(None, {'fields': ['owner']}),
          #(None, {'fields': ['friends']}),
      #]
      #list_display = ('name', 'owner',)

admin.site.register(GroupAccountInvite, GroupAccountInviteAdmin)

#admin.site.register(Account, AccountAdmin)
