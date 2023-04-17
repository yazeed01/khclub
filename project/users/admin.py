from .models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *



@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("name", "email", "is_superuser", "is_staff", "is_active", "date_joined")
    list_display_links = ("email",)
    search_fields = ("name", "bio", "email")
    search_help_text = "ابحث بـ : الاسم كامل، البريد الإلكتروني"

    ordering = ("name",)

    fieldsets = (
        (None, {"fields": ("name", "password")}),
        ("Personal info", {"fields": ("email", "bio", "image")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("name", "password1", "password2"),
            },
        ),
    )

from django.utils.html import format_html

class CustomPersonnel(admin.ModelAdmin):
    list_display = ("name", "type_user","who_i", "display",'image_tag',"join_us",)
    search_fields = ("name", "type_user",)
    search_help_text = "ابحث بـ : الاسم، الفئة"
    list_filter = ("display", "type_user", "join_us")
    list_editable = ("display",)
    readonly_fields = ('image_tag',)
    
    def image_tag(self, obj):
        if obj.image:
            return format_html('<a href="/media/{}"><img src="/media/{}" width="70" height="50"/></a>'.format(obj.image, obj.image))
        else:
            return "لا توجد صورة"
    image_tag.short_description = 'عرض الصورة'
    image_tag.allow_tags = True


class CustomPartners(admin.ModelAdmin):
    list_display = ("name", "date_start","who_i", 'image_tag', "display", "join_us",)
    search_fields = ("name",)
    search_help_text = "ابحث بـ : اسم الشريك"
    list_filter = ("display", "join_us")
    list_editable = ("display",)
    readonly_fields = ('image_tag',)
    
    def image_tag(self, obj):
        if obj.image:
            return format_html('<a href="/media/{}"><img src="/media/{}" width="70" height="50"/></a>'.format(obj.image, obj.image))
        else: return "لا توجد صورة"
    image_tag.short_description = 'عرض الصورة'
    image_tag.allow_tags = True




admin.site.register(Personnel, CustomPersonnel)
admin.site.register(Partners, CustomPartners)
