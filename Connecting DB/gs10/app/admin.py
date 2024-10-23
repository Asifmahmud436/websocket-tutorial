from django.contrib import admin
from .models import Chat,Group

@admin.register(Chat)
class ChatModelAdmin(admin.ModelAdmin):
    list_display = ['id','content','timestamp','group']
    
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id','name']