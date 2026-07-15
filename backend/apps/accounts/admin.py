from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class HogarExpressUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Hogar Express",
            {
                "fields": (
                    "display_name",
                    "must_change_password",
                    "failed_login_attempts",
                    "locked_until",
                    "last_password_change",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (("Hogar Express", {"fields": ("email", "display_name")}),)
    list_display = ("username", "display_name", "email", "is_active", "is_staff", "last_login")
    search_fields = ("username", "display_name", "email")
