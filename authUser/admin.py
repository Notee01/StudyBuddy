from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class MyUserChangeForm(UserAdmin.form):
    password = None
    class Meta:
        model = User
        fields = '__all__'

class MyUserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'username', 'name',)
    list_filter = ('email', 'username', 'name', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'username', 'name', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'name', 'password1', 'password2', 'is_active', 'is_staff')
        }),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not obj:  
            return fieldsets
        return [(name, values) for name, values in fieldsets if name != 'password']

admin.site.register(User, MyUserAdminConfig)
