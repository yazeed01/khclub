
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

def arabic_slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("؟", "")
    return str

class Period(models.Model):
    name = models.CharField("عنوان الفترة" ,max_length=255)
    date_start = models.DateField("تاريخ البدء")
    date_end = models.DateField("تاريخ الانتهاء")
    display  = models.BooleanField("تفعيل؟", help_text="سوف تظهر الفترة المفعلة فقط في الرسمة البيانية في الصفحة الرئيسية لاعلى خمس نقاط (علما ان يمكنك تفعيل فترة واحده فقط)")

    class Meta:
        verbose_name = ('الفترة')
        verbose_name_plural = ('الفترات')   
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.display:
            try:
                temp = Period.objects.get(display=True)
                if temp:
                    temp.display = False
                    temp.save()
            except Period.DoesNotExist:
                pass
        super(Period, self).save(*args, **kwargs)

class Quiz(models.Model):
    name = models.CharField("العنوان",max_length=255)
    date_start = models.DateField("تاريخ البدء")
    date_end = models.DateField("تاريخ الانتهاء")
    period = models.ForeignKey(Period, verbose_name="الفترة", on_delete=models.CASCADE)
    display  = models.BooleanField("إظهار؟", default=True)
    created_at = models.DateTimeField("تاريخ الإنشاء", auto_now_add=True)
    slug = models.SlugField(allow_unicode=True, blank=True, null=True)
    
    class Meta:
        verbose_name = ('النموذج')
        verbose_name_plural = ('نماذج')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = arabic_slugify(self.name)
        super(Quiz, self).save(*args, **kwargs)

    def get_if_ans(self):
        return CorrectAnswer.objects.select_related('correct_answer').filter(correct_answer__question__quiz=self)


class Questions(models.Model):
    quiz = models.ForeignKey(Quiz, verbose_name="النموذج", null=False, on_delete=models.CASCADE)
    tyep = models.CharField("نوع السؤال", max_length=255, help_text=("مثل: عام ، رياضيات ، فيزياء، .."))
    text = RichTextField("السؤال", blank=False, null=False)
    created_at = models.DateTimeField("تاريخ الإنشاء", auto_now_add=True)

    class Meta:
        verbose_name = ('السؤال')
        verbose_name_plural = ('أسئلة')
    
    def get_answers(self):
        return Answers.objects.filter(question=self)
    
    def __str__(self):
        return self.text

class Answers(models.Model):
    question = models.ForeignKey(Questions, verbose_name="السؤال", on_delete=models.CASCADE)
    text = models.CharField("الجواب", max_length=255, null=False, blank=False)
    is_correct = models.BooleanField("الجواب الصحيح؟", default=False, null=False, blank=False)
    created_at = models.DateTimeField("تاريخ الإنشاء", auto_now_add=True)

    class Meta:
        verbose_name = ('جواب')
        verbose_name_plural = ('الإجابات')
    
    def __str__(self):
        return self.text

class CorrectAnswer(models.Model):
    correct_answer = models.ForeignKey(Answers, verbose_name="جواب المستخدم", on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="اسم المستخدم", on_delete=models.CASCADE)
    created_at = models.DateTimeField("تاريخ الإنشاء", auto_now_add=True)

    class Meta:
        verbose_name = ('الجواب الصحيح')
        verbose_name_plural = ('إجابات المستخدمين')
    
    def __str__(self):
        return f"{self.created_by} الجواب {self.correct_answer}"
    
    @property
    def get_points(self):
        point = self.points_set.get()
        return str(point.proints)

    def get_point(self):
        return Points.objects.filter(correct_answer_point=self)


class Points(models.Model):
    correct_answer_point = models.ForeignKey(CorrectAnswer, on_delete=models.CASCADE)
    proints= models.IntegerField("النقطة", max_length=10, blank=True , null=True)
    
    class Meta:
        verbose_name = ('النقطة')
        verbose_name_plural = ('النقاط')
