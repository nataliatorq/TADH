from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import BaseUser, Customer, Jogo, Offensiva


class BaseUserAdmin(UserAdmin):
    model = BaseUser
    list_display = ['username', 'email', 'is_staff']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('birth_date', 'photo')}),
    )

admin.site.register(BaseUser, BaseUserAdmin)
admin.site.register(Jogo)
admin.site.register(Customer)
admin.site.register(Offensiva)