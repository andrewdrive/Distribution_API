from turtle import circle
from django.contrib import admin
from api.models import Distribution, Client, Message


admin.site.register(Distribution, admin.ModelAdmin)
admin.site.register(Client, admin.ModelAdmin)
admin.site.register(Message, admin.ModelAdmin)


# Register your models here.
