from django.db import models
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
User = get_user_model()

class Category(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('videos', 'فديوهات'),
        ('photos', 'صور'),
        ('VideosPhotos', 'فديوهات و صور'),
    ]
    
    title = models.CharField("الفئة", max_length=50)
    content_type = models.CharField("نوع المحتوى",max_length=12, choices=CONTENT_TYPE_CHOICES)
    display  = models.BooleanField("إظهار؟", default=False)
    created_in = models.DateTimeField("تاريخ الانشاء", auto_now_add=True, blank=True, null=True)

    slug = models.SlugField(allow_unicode=True, blank=True, null=True)

    class Meta:
        verbose_name = ('فئة')
        verbose_name_plural = ('الفئات')
    
    def save(self, *args, **kwargs):
        self.slug = arabic_slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


def arabic_slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("؟", "")
    return str

class Data_Category(models.Model):
    title = models.TextField("العنوان", max_length=300, blank=True , null=True)
    describe = models.TextField("الوصف (اختياري)", blank=True , null=True)
    image = models.ImageField("الصورة (اختياري)", upload_to="Data_Category_image", blank=True , null=True)
    url_video = models.URLField("رابط الفيديو (اختياري)", blank=True, null=True, help_text=("ملاحظة: ازل \"=watch?v\" من الرابط و اضع \"/embed/ \" مثل: https://www.youtube.com/watch?v=S709PX3u5AA إلى: https://www.youtube.com/embed/S709PX3u5AA"))
    created_in = models.DateTimeField("تاريخ الانشاء", auto_now_add=True, blank=True, null=True)
    category = models.ForeignKey(Category, verbose_name="الفئة", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="الكاتب", on_delete=models.CASCADE)
    display  = models.BooleanField("إظهار؟", default=False)


    class Meta:
        verbose_name = ('محتوى')
        verbose_name_plural = ('المحتوى')

    def __str__(self):
        return "الموافقة على نشر " + "(" + self.title + ")"

class ApprovalData_Category(models.Model):
    APPROVAL = "AP"
    UNACCEPTABLE = "UN"
    PENDING = "PE"
    STATUS = [
        (APPROVAL, 'موافق'),
        (UNACCEPTABLE, 'مرفوض'),
        (PENDING, 'قيد الانتظار'),
    ]
    data_category = models.ForeignKey(Data_Category, verbose_name="المحتوى", unique=True, on_delete=models.CASCADE)
    approval = models.CharField("الموافقة", max_length=2, choices=STATUS, default=PENDING)
    created_in = models.DateTimeField("تاريخ الانشاء", auto_now_add=True, blank=True, null=True)


    @receiver(post_save, sender=Data_Category) 
    def create_profile(sender, instance, created, **kwargs):
        if created:
            ApprovalData_Category.objects.create(data_category=instance)

    class Meta:
        verbose_name = ('موافقة')
        verbose_name_plural = ('موافقات المحتوى')

    def __str__(self):
        return "الموافقة على نشر " + "(" + self.data_category.title + ")"