from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import OpticUser,Account,EmployeeUser
from django.contrib.auth.models import Permission

# Register your models here.
# @admin.register(OpticUser)
# class CustomUserAdmin(UserAdmin):
#     list_display = ('id','email','full_name','optic','is_staff','is_active','is_superuser')
#     fieldsets = (
#         (None, {'fields': ([field.name for field in OpticUser._meta.get_fields() if (field.name!='logentry' and field.name!='id')])}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active','optic')}
#         ),
#     )
#     search_fields = ('email',)
#     ordering = ('email',)

class AdminAccount(admin.ModelAdmin):
    search_fields=['username','full_name']

admin.site.register(Account,AdminAccount)
admin.site.register(OpticUser)
admin.site.register(EmployeeUser)
admin.site.register(Permission)