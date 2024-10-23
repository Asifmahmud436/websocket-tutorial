from django.shortcuts import render
from .models import Chat,Group

def index(request,group_name):
    # Get or create the group
    group, created = Group.objects.get_or_create(name=group_name)

    # Retrieve chats for the group
    chats = Chat.objects.filter(group=group)

    return render(request, 'app/index.html', {
        'groupname': group_name,
        'chats': chats
    })