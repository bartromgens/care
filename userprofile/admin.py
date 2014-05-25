from userprofile.models import UserProfile
#from accounts.models import Account
from django.contrib import admin

class UserProfileAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['user']}),
    (None, {'fields': ['displayname']}),
    (None, {'fields': ['groupAccounts']}),
  ]
  
  list_display = ('user', 'displayname',)
    
#class AccountAdmin(admin.ModelAdmin):
    #fieldsets = [
        #(None, {'fields': ['name']}),
        #(None, {'fields': ['owner']}),
        #(None, {'fields': ['friends']}),
    #]
    #list_display = ('name', 'owner',)

admin.site.register(UserProfile, UserProfileAdmin)

#admin.site.register(Account, AccountAdmin)
