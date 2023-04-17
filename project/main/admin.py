from django.contrib import admin

from .models import Blog, News, NewsSlide, Contact_Me, ApprovalBlog, ApprovalNews, PermissionsApprovals
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from django.contrib import messages

from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib import messages
from django.utils.translation import ngettext





@admin.register(PermissionsApprovals)
class CustomPermissionsApprovals(admin.ModelAdmin):
    list_display = ("user", "content", "approval", "created_in")
    search_fields = ("user", "content",)
    list_filter = ("content", "created_in",)
    search_help_text = "ابحث بـ المستخدم، الموافقة في"

    def save_model(self, request, obj, form, change):
        P_A = None
        try:
            P_A = PermissionsApprovals.objects.get(user=obj.user, content=obj.content)
            if P_A:
                if change:
                    super(CustomPermissionsApprovals, self).save_model(request, obj, form, change)
                else:
                    messages.add_message(request, messages.WARNING, mark_safe(f"الأذن موجود مسبقا <b>\"{P_A}\"</b>"))
                
            else:
                super(CustomPermissionsApprovals, self).save_model(request, obj, form, change)
        except PermissionsApprovals.DoesNotExist:
            super(CustomPermissionsApprovals, self).save_model(request, obj, form, change)
        except PermissionsApprovals.MultipleObjectsReturned:
            messages.add_message(request, messages.WARNING, mark_safe(f"الأذن موجود مسبقا <b>\"{P_A}\"</b>"))

        # if P_A:
        #     messages.add_message(request, messages.WARNING, mark_safe(f"ssssssssالأذن موجود مسبقا <b>\"{P_A}\"</b>"))
        # else:
        #     super(CustomPermissionsApprovals, self).save_model(request, obj, form, change)


@admin.register(Contact_Me)
class CustomContact_Me(admin.ModelAdmin):
    list_display = ("first_name", "email", "message", "created_in")
    search_fields = ("first_name",)
    search_help_text = "ابحث بـ : الاسم كامل"
    list_filter = ("created_in",)


@admin.register(Blog)
class CustomBlog(admin.ModelAdmin):
    list_display = ("title", "image_tag", "url_video_tag", "author", "display", "approval", "created_in")
    search_fields = ("title", "author__name",)
    search_help_text = "ابحث بـ : العنوان، الكاتب"
    list_filter = ("display", "created_in",)
    list_editable = ("display",)
    readonly_fields = ("author", "image_tag", "approval", "slug")
    actions = ['display_ac','undisplay_ac']


    @admin.action(description='إظهار المدونة المحددة')
    def display_ac(self, request, queryset):
        updated = queryset.update(display=True)
        self.message_user(request, ngettext(
            '%d تم اظهار مدونة نجاح.',
            '%d  تم اظهار مدونة نجاح.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='إخفاء المدونة المحددة')
    def undisplay_ac(self, request, queryset):
        updated = queryset.update(display=False)
        self.message_user(request, ngettext(
            '%d تم إخفاء مدونة نجاح.',
            '%d  تم إخفاء مدونة نجاح.',
            updated,
        ) % updated, messages.SUCCESS)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "author":
    #         if not request.user.is_superuser:
    #             kwargs["queryset"] = User.objects.filter(name=request.user.name)
    #         return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def approval(self, obj):
        appro = ApprovalBlog.objects.get(blog=obj).approval
        if appro == "AP":
            return format_html("<p style='color:#2abd57;'>موافق</p>")
        elif appro == "UN":
            return format_html("<p style='color:#f00;'>مرفوض</p>")
        else: 
            return format_html("<p style='color:#e18f2a;'>قيد الانتظار</p>")
    approval.short_description = 'الموافقة'
    approval.allow_tags = True


    def image_tag(self, obj):
        if obj.image:
            return format_html('<a href="/media/{}"><img src="/media/{}" width="70" height="50"/></a>'.format(obj.image, obj.image))
        else: return "لا توجد صورة"
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
            messages.success(request, "الرجاء اختيار صورة او فيديو لا يأتي صورة مع فيديو")
            obj.display = False
        else:
            super(CustomBlog, self).save_model(request, obj, form, change)
            try:
                if not request.user.is_superuser:
                    PermissionsApprovals.objects.get(user=request.user, content="BL", approval=True)
                    A_B, A_B_created = ApprovalBlog.objects.get_or_create(blog=obj)
                    A_B.approval = "AP"
                    A_B.save()
                # else:
                    # A_B, A_N_created = ApprovalBlog.objects.get_or_create(blog=obj)
                    # A_B.approval = "AP"
                    # A_B.save()
            except PermissionsApprovals.DoesNotExist:
                pass

@admin.register(ApprovalBlog)
class CustomApprovalBlog(admin.ModelAdmin):
    list_display = ("blog", "approval", "created_in")
    search_fields = ("blog__title", "blog__author__name",)
    list_filter = ("approval","created_in",)
    search_help_text = "ابحث بـ : التدوينة ، الكاتب"
    list_editable = ("approval",)
    actions = ['approval_ac','unapproval_ac']
    
    @admin.action(description='موافق موافقات التدوينات المحددة')
    def approval_ac(self, request, queryset):
        updated = queryset.update(approval="AP")
        self.message_user(request, ngettext(
            '%d تم قبول نشر التدوينات .',
            '%d تم قبول نشر التدوينات .',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='مرفوض موافقات التدوينات المحددة')
    def unapproval_ac(self, request, queryset):
        updated = queryset.update(approval="UN")
        self.message_user(request, ngettext(
            '%d تم رفض نشر التدوينات .',
            '%d تم رفض نشر التدوينات .',
            updated,
        ) % updated, messages.SUCCESS)



@admin.register(News)
class CustomNews(admin.ModelAdmin):
    list_display = ("title", "image_tag", "author", "display", "approval",  "created_in")
    search_fields = ("title", "author__name",)
    search_help_text = "ابحث بـ : العنوان، الكاتب"
    list_filter = ("display", "created_in",)
    list_editable = ("display",)
    readonly_fields = ("author","image_tag", "slug")
    actions = ['display_ac','undisplay_ac']
    
    @admin.action(description='إظهار الخبر المحددة')
    def display_ac(self, request, queryset):
        updated = queryset.update(display=True)
        self.message_user(request, ngettext(
            '%d تم اظهار خبر نجاح.',
            '%d  تم اظهار خبر نجاح.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='إخفاء الخبر المحددة')
    def undisplay_ac(self, request, queryset):
        updated = queryset.update(display=False)
        self.message_user(request, ngettext(
            '%d تم إخفاء خبر .',
            '%d  تم إخفاء خبر .',
            updated,
        ) % updated, messages.SUCCESS)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
    
    def approval(self, obj):
        appro = ApprovalNews.objects.get(news=obj).approval
        if appro == "AP":
            return format_html("<p style='color:#2abd57;'>موافق</p>")
        elif appro == "UN":
            return format_html("<p style='color:#f00;'>مرفوض</p>")
        else: 
            return format_html("<p style='color:#e18f2a;'>قيد الانتظار</p>")
    approval.short_description = 'الموافقة'
    approval.allow_tags = True
    
    
    def image_tag(self, obj):
        if obj.image:
            return format_html('<a href="/media/{}"><img src="/media/{}" width="70" height="50"/></a>'.format(obj.image, obj.image))
        else: return "لا توجد صورة"
    image_tag.short_description = 'عرض الصورة'
    image_tag.allow_tags = True


    def save_model(self, request, obj, form, change):
        if change:
            if not request.user.is_superuser:
                obj.author = request.user
        else:
            obj.author = request.user
        super(CustomNews, self).save_model(request, obj, form, change)
        
        try:
            if request.user.is_superuser:
                PermissionsApprovals.objects.get(user=request.user, content="NE", approval=True)
                A_N, A_N_created = ApprovalNews.objects.get_or_create(news=obj)
                A_N.approval = "AP"
                A_N.save()
        except PermissionsApprovals.DoesNotExist:
            pass


@admin.register(ApprovalNews)
class CustomApprovalNews(admin.ModelAdmin):
    list_display = ("news", "approval", "created_in")
    search_fields = ("news__title", "news__author__name",)
    list_filter = ("approval","created_in",)
    search_help_text = "ابحث بـ : الخبر ، الكاتب"
    list_editable = ("approval",)
    actions = ['approval_ac','unapproval_ac']
    
    @admin.action(description='قبول موافقات الاخبار المحددة')
    def approval_ac(self, request, queryset):
        updated = queryset.update(approval="AP")
        self.message_user(request, ngettext(
            '%d تم قبول على نشر الخبر نجاح.',
            '%d تم قبول على نشر الخبر نجاح.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='رفض موافقات الاخبار المحددة')
    def unapproval_ac(self, request, queryset):
        updated = queryset.update(approval="UN")
        self.message_user(request, ngettext(
            '%d تم رفض نشر الخبر .',
            '%d تم رفض نشر الخبر .',
            updated,
        ) % updated, messages.SUCCESS)
        


@admin.register(NewsSlide)
class CustomNewsSlide(admin.ModelAdmin):
    list_display = ("id","image_tag",)

    def image_tag(self, obj):
        return format_html('<a href="/media/{}"><img src="/media/{}" width="150" height="100"/></a>'.format(obj.image, obj.image))
    image_tag.short_description = 'عرض الصورة'
    image_tag.allow_tags = True