from django.contrib import admin

from care.groupaccount.models import GroupAccount, GroupSetting


class GroupAccountAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['number']}),
        (None, {'fields': ['name']}),
        (None, {'fields': ['settings']}),
    ]
    list_display = ('id', 'name', 'number')


class GroupSettingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['notification_lower_limit']}),
        (None, {'fields': ['notification_lower_limit_interval']}),
    ]
    list_display = ('id', 'notification_lower_limit', 'notification_lower_limit_interval')

#class AccountAdmin(admin.ModelAdmin):
    #fieldsets = [
        #(None, {'fields': ['name']}),
        #(None, {'fields': ['owner']}),
        #(None, {'fields': ['friends']}),
    #]
    #list_display = ('name', 'owner',)

admin.site.register(GroupAccount, GroupAccountAdmin)
admin.site.register(GroupSetting, GroupSettingAdmin)

#admin.site.register(Account, AccountAdmin)
