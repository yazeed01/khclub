from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User, AbstractUser, BaseUserManager, Group
from django.db.models.signals import post_save
from django.urls import reverse
from django.conf import settings


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    # remove default fields
    username = None
    first_name = None
    last_name = None

    email = models.EmailField("البريد الإلكتروني", unique=True)
    name = models.CharField("الاسم كامل", unique=True, max_length=40)
    bio = models.TextField("السيرة الذاتية", null=True, blank=True)
    image = models.ImageField(("الصورة"), upload_to='user-image', null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = ('مستخدم')
        verbose_name_plural = ('المستخدمين')

    objects = CustomUserManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("profile", args=[self.id])

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name


class Personnel(models.Model):
    name = models.CharField("الاسم", max_length=80)
    type_user = models.CharField("الفئة", max_length=40,  help_text=('مثل: مؤسس , عضو , رئيس , ..'))
    who_i = models.TextField(("السيره الذاتيه (إختياري)"), max_length=300, blank=True, null=True)
    image = models.ImageField(("الصورة (إختياري)"), upload_to='personnel-image', blank=True, null=True)
    order = models.IntegerField("الترتيب", unique=True, blank=False, null=False, max_length=100)
    display  = models.BooleanField("إظهار؟", default=True, help_text=('إظهار العنصر او إخفاء.'))
    join_us = models.DateTimeField("تاريخ الإنشاء", auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = ('عضو')
        verbose_name_plural = ('فريق العمل')
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


    def __str__(self):
        return self.name



class Partners(models.Model):
    name = models.CharField("اسم الشريك",max_length=80)
    image = models.ImageField(("الصوره"), upload_to='partners-image')
    who_i = models.TextField(("معلومات عن الشريك (إختياري)"), max_length=300, blank=True, null=True)
    date_start = models.DateField(("تاريخ انضمام الشريك (إختياري) "), blank=True, null=True)
    join_us = models.DateTimeField("تاريخ الإنشاء", auto_now_add=True, blank=True, null=True)
    display  = models.BooleanField("إظهار؟", default=True)

    class Meta:
        verbose_name = ('شريك')
        verbose_name_plural = ('الشركاء')

    def __str__(self):
        return self.name