from django.contrib import admin
from django.urls import reverse
from . models import Category, Data_Category, ApprovalData_Category
from django.utils.html import format_html
from main.models import PermissionsApprovals
from django.contrib import messages
from django.utils.translation import ngettext



@admin.register(Data_Category)
class CustomData_Category(admin.ModelAdmin):
    list_display = ("id","title", "describe_def", "category", "content_type", "image_tag", "url_video_tag", "author", "approval", "display", "created_in")
    search_fields = ("title", "author__name",)
    search_help_text = "ابحث بـ : العنوان ، الكاتب"
    list_filter = ("display", "category__content_type", "category", "created_in")
    list_editable = ("display",)
    readonly_fields = ('image_tag', "author", "url_video_tag")
    list_per_page = 15
    actions = ['display_ac','undisplay_ac']

    @admin.action(description='إظهار المحتوى المحددة')
    def display_ac(self, request, queryset):
        updated = queryset.update(display=True)
        self.message_user(request, ngettext(
            '%d تم اظهار محتوى نجاح.',
            '%d  تم اظهار محتوى نجاح.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='إخفاء المحتوى المحددة')
    def undisplay_ac(self, request, queryset):
        updated = queryset.update(display=False)
        self.message_user(request, ngettext(
            '%d تم إخفاء محتوى نجاح.',
            '%d  تم إخفاء محتوى نجاح.',
            updated,
        ) % updated, messages.SUCCESS)
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def approval(self, obj):
        appro = ApprovalData_Category.objects.get(data_category=obj).approval
        if appro == "AP":
            return format_html("<p style='color:#2abd57;'>موافق</p>")
        elif appro == "UN":
            return format_html("<p style='color:#f00;'>مرفوض</p>")
        else: 
            return format_html("<p style='color:#e18f2a;'>قيد الانتظار</p>")
    approval.short_description = 'الموافقة'
    approval.allow_tags = True

    @admin.display(description='الوصف')
    def describe_def(self, obj):
        if obj.describe and obj.describe[:40]:
            return obj.describe[:40] + "..."

    @admin.display(description='نوع المحتوى')
    def content_type(self, obj):
        if obj.category.content_type == "videos":return "فديوهات"
        elif obj.category.content_type == "photos":return "صور"
        else:return "فديوهات و صور"
    
    def image_tag(self, obj):
        if obj.image:
            return format_html('<a href="/media/{}"><img src="/media/{}" width="70" height="50"/></a>'.format(obj.image, obj.image))
        else: return "-"
    image_tag.short_description = 'عرض الصورة'
    image_tag.allow_tags = True
    
    def url_video_tag(self, obj):
        if obj.url_video:
            return format_html('<a href="{}">مشاهدة الفيديو</a>'.format(obj.url_video))
        else: return "-"
    url_video_tag.short_description = 'رابط الفيديو'
    url_video_tag.allow_tags = True
    

    def save_model(self, request, obj, form, change):
        if change:
            if not request.user.is_superuser:
                obj.author = request.user
        else:
            obj.author = request.user
        
        if obj.image and obj.url_video:
            messages.warning(request, "الرجاء اختيار صورة او فيديو لا يأتي صورة مع فيديو")
        else:
            super(CustomData_Category, self).save_model(request, obj, form, change)
            try:
                if not request.user.is_superuser:
                    PermissionsApprovals.objects.get(user=request.user, content="DC", approval=True)
                    A_B, A_B_created = ApprovalData_Category.objects.get_or_create(data_category=obj)
                    A_B.approval = "AP"
                    A_B.save()
                # else:
                #     A_B, A_N_created = ApprovalData_Category.objects.get_or_create(data_category=obj)
                #     A_B.approval = "AP"
                #     A_B.save()
            except PermissionsApprovals.DoesNotExist:
                pass


@admin.register(ApprovalData_Category)
class CustomApprovalData_Category(admin.ModelAdmin):
    list_display = ("data_category", "approval", "created_in")
    list_filter = ("approval", "created_in",)
    list_editable = ("approval",)
    autocomplete_fields = ('data_category',)
    search_fields = ("data_category__title","created_in", "data_category__author__name",)
    search_help_text = "ابحث بـ : المحتوى ، الكاتب"
    actions = ['approval_ac','unapproval_ac']
    
    @admin.action(description='قبول موافقات المحتوى المحددة')
    def approval_ac(self, request, queryset):
        updated = queryset.update(approval="AP")
        self.message_user(request, ngettext(
            '%d تم قبول على نشر المحتوى نجاح.',
            '%d تم قبول على نشر المحتوى نجاح.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='رفض موافقات المحتوى المحددة')
    def unapproval_ac(self, request, queryset):
        updated = queryset.update(approval="UN")
        self.message_user(request, ngettext(
            '%d تم رفض نشر المحتوى .',
            '%d تم رفض نشر المحتوى .',
            updated,
        ) % updated, messages.SUCCESS)

@admin.register(Category)
class CustomCategory(admin.ModelAdmin):
    list_display = ("title", "content_type", "display", "created_in")
    search_fields = ("title",)
    search_help_text = "ابحث بـ : الفئة"
    list_filter = ("display", "content_type", "created_in")
    readonly_fields = ("slug",)
    list_editable = ("display",)
    list_per_page = 15



