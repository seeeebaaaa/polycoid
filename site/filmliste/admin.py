from django.contrib import admin
from filmliste.models import CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.

# @admin.register(CustomUser)
# class MyUserAdmin(UserAdmin):
#         model = CustomUser
#         list_display = ('username',
#                         'email')
#         list_filter = ('username',
#                         'email')
#         search_fields = ('username', )
#         ordering = ('username', )
#         filter_horizontal = ()
#         fieldsets = UserAdmin.fieldsets + (
#                 (None, {'fields': ('username',)}),
#         )
#         # I've added this 'add_fieldset'
#         add_fieldsets = (
#             (None, {
#                 'classes': ('wide',),
#                 'fields': ('username', 'password1', 'password2'),
#             }),
#     )