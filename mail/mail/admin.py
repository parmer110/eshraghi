from django.contrib import admin
from .models import User, Email
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    list_editable = ("username", "email")

class EmailAdmin(admin.ModelAdmin):
    fields = ["sender"]
    list_display = ("id", "user", "sender",  "recipientss", "subject", "body", "timestamp", "read", "archived")
    list_display_links = ['user']
    list_editable = ("subject","read", "archived")

    def recipientss(self, obj):
        return "\n".join([str(r.username) for r in obj.recipients.all()])    

admin.site.register(User, UserAdmin)
admin.site.register(Email, EmailAdmin)
