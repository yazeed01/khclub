from datetime import timezone
from pydoc import describe

from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.exceptions import ValidationError


class Blog(models.Model):
    title = models.CharField("العنوان", max_length=50, blank=False, null=False)
    body = RichTextField("المقال", blank=False, null=False)
    image = models.ImageField("صورة (اختياري)", upload_to="blog_image", blank=True, null=True)
    url_video = models.URLField("فيديو (اختياري)", blank=True , null=True, help_text=("ملاحظة: ازل \"=watch?v\" من الرابط و اضع \"/embed/ \" مثل: https://www.youtube.com/watch?v=S709PX3u5AA إلى: https://www.youtube.com/embed/S709PX3u5AA"))
    created_in = models.DateTimeField("تاريخ الانشاء", auto_now_add=True, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="الكاتب", on_delete=models.CASCADE)
    display  = models.BooleanField("إظهار / إخفاء ؟", default=False)
    slug = models.SlugField(allow_unicode=True, blank=False, null=False)
    
    class Meta:
        verbose_name = ('تدوينة')
        verbose_name_plural = ('المدونة')

    def save(self, *args, **kwargs):
        self.slug = arabic_slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class ApprovalBlog(models.Model):
    APPROVAL = "AP"
    UNACCEPTABLE = "UN"
    PENDING = "PE"
    STATUS = [
        (APPROVAL, 'موافق'),
        (UNACCEPTABLE, 'مرفوض'),
        (PENDING, 'قيد الانتظار'),
    ]
    blog = models.ForeignKey(Blog, verbose_name="التدوينة", unique=True, on_delete=models.CASCADE)
    approval = models.CharField("الموافقة", max_length=2, choices=STATUS, default=PENDING)
    created_in = models.DateTimeField("تاريخ الانشاء", auto_now_add=True, blank=True, null=True)


    @receiver(post_save, sender=Blog) 
    def create_profile(sender, instance, created, **kwargs):
        if created:
            ApprovalBlog.objects.create(blog=instance)

    def __str__(self):
        return "الموافقة على نشر " + "(" + self.blog.title + ")"

    class Meta:
        verbose_name = ('موافقة')
        verbose_name_plural = ('موافقات التدوينات')


def arabic_slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("؟", "")
    return str

class News(models.Model):
    title = models.CharField("العنوان", max_length=50)
    body = RichTextField("الخبر", blank=True, null=True)
    image = models.ImageField("صورة (اختياري)", upload_to="news_image", blank=True, null=True)
    created_in = models.DateTimeField("تاريخ الانشاء", auto_now_add=True, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="الكاتب", on_delete=models.CASCADE)
    display  = models.BooleanField("إظهار / إخفاء ؟", default=True)
    slug = models.SlugField(allow_unicode=True, blank=True, null=True)
    
    class Meta:
        verbose_name = ('خبر')
        verbose_name_plural = ('الأخبار')
    
    def save(self, *args, **kwargs):
        self.slug = arabic_slugify(self.title)
        super(News, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title

def validate_image(image):
    if image.width != 1108 and image.height != 428:
        raise ValidationError("المقاس المناسب للصورة هو (428 * 1108)")

class NewsSlide(models.Model):
    image = models.ImageField("صورة", upload_to="news_slide", validators=[validate_image], help_text="المقاس المناسب للصورة هو (428 * 1108)", blank=False, null=False)
    
    class Meta:
        verbose_name = ('شريحة خبر')
        verbose_name_plural = ('شريحة الأخبار')

class ApprovalNews(models.Model):
    APPROVAL = "AP"
    UNACCEPTABLE = "UN"
    PENDING = "PE"
    STATUS = [
        (APPROVAL, 'موافق'),
        (UNACCEPTABLE, 'مرفوض'),
        (PENDING, 'قيد الانتظار'),
    ]
    news = models.ForeignKey(News, verbose_name="الخبر", unique=True, on_delete=models.CASCADE)
    approval = models.CharField("الموافقة", max_length=2, choices=STATUS, default=PENDING)
    created_in = models.DateTimeField("تاريخ الانشاء", auto_now_add=True, blank=True, null=True)


    @receiver(post_save, sender=News) 
    def create_profile(sender, instance, created, **kwargs):
        if created:
            ApprovalNews.objects.create(news=instance)

    def __str__(self):
        return "الموافقة على نشر " + "(" + self.news.title + ")"

    class Meta:
        verbose_name = ('موافقة')
        verbose_name_plural = ('موافقات الاخبار')

class Contact_Me(models.Model):
    first_name = models.CharField(("الاسم الاول"), max_length=50, blank=False, null=False)
    email = models.EmailField(("البريد الألكترونى"), max_length=254, blank=False, null=False)    
    message = models.TextField(("الرسالة"))
    created_in = models.DateTimeField("تاريخ الانشاء", auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = ('اتصل بنا')
        verbose_name_plural = ('اتصل بنا')
    
    def __str__(self):
        return self.first_name


class PermissionsApprovals(models.Model):
    NEWS = "NE"
    BLOG = "BL"
    DATA_CATEGORY = "DC"
    STATUS_P_A = [
        (NEWS, 'الاخبار'),
        (BLOG, 'المدونة'),
        (DATA_CATEGORY, 'المحتوى'),

    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="المستخدم", on_delete=models.CASCADE)
    content = models.CharField("الموافقة في", max_length=2, choices=STATUS_P_A)
    approval = models.BooleanField("الموافقة", default=True)
    created_in = models.DateTimeField("تاريخ الانشاء", auto_now_add=True, blank=True, null=True)


    class Meta:
        verbose_name = ('موافقات الأذونات')
        verbose_name_plural = ('موافقات الأذونات')
    
    def __str__(self):
        if self.content == "BL": op = "المدونة"
        elif self.content == "NE": op = "الاخبار"
        else: op = "المحتوى"
        return f"الموافقة على {self.user} دون طلب الموافقة في ({op})"