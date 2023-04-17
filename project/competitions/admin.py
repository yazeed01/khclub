from django.contrib import admin
from .models import Answers, Questions, Quiz, CorrectAnswer, Points, Period
from django.utils.html import format_html

# Register your models here.


class QuestionsInline(admin.TabularInline):
    model = Questions
    def get_max_num(self, request, obj=None, **kwargs):
        max_num = 1
        return max_num


class AnswersInline(admin.TabularInline):
    model = Answers
    def get_max_num(self, request, obj=None, **kwargs):
        max_num = 3
        return max_num


class CustomQuestions(admin.ModelAdmin):
    inlines = [AnswersInline]
    list_display = ("text", "tyep", "quiz", "answers", "correct_answer", "created_at",)
    search_fields = ("text", "quiz__name")
    search_help_text = "ابحث بـ : السؤال، النموذج"
    list_filter = ("created_at", "tyep")
    list_per_page = 15

    def answers(self, obj):
        s = Answers.objects.filter(question=obj)
        if s: return [i.text for i in s]
    answers.short_description = "الإجابات"
    
    def correct_answer(self, obj):
        return Answers.objects.get(is_correct=True, question=obj)
    correct_answer.short_description = "الجواب الصحيحة"


class CustomAnswers(admin.ModelAdmin):
    list_display = ("quiz", "question", "text", "is_correct", "created_at",)
    search_fields = ("question__text", "question__quiz__name")
    search_help_text = "ابحث بـ : النموذج، السؤال"
    list_filter = ("created_at",)
    list_display_links = ("text",)
    list_per_page = 15
    
    def quiz(self, obj):
        return obj.question.quiz
    quiz.short_description = "النموذج"


class CustomCorrectAnswer(admin.ModelAdmin):
    list_display = ("created_by", "period", "quiz", "question", "correct_answer", "mark", "the_correct_answer", "points","created_at")
    list_filter = ("created_at", "correct_answer__is_correct")
    search_fields = ("created_by__name", "correct_answer__question__text", "correct_answer__question__quiz__name")
    search_help_text = "ابحث بـ : النموذج، السؤال، اسم المستخدم"
    list_per_page = 15
    
    
    
    def points(self, obj):
        if po:= Points.objects.get(correct_answer_point=obj).proints:
            return po
        else: 
            return "0"
    points.short_description = "النقطة"

    def period(self, obj):
        return obj.correct_answer.question.quiz.period
    period.short_description = "الفترة"
    
    def quiz(self, obj):
        return obj.correct_answer.question.quiz
    quiz.short_description = "النموذج"
    
    def question(self, obj):
        return obj.correct_answer.question
    question.short_description = "السؤال"
    
    def the_correct_answer(self, obj):
        return [i for i in Answers.objects.filter(is_correct=True, question=obj.correct_answer.question)]
    the_correct_answer.short_description = "الجواب الصحيحة"

    def mark(self, obj):
        if obj.correct_answer.is_correct == True: return format_html("<span style='color:#00ff4e;'>&#10004;</apan>")
        else: return format_html("<span style='color:#f00;'>&#10006;</apan>")
    mark.short_description = "العلامة"


class CustomQuiz(admin.ModelAdmin):
    inlines = [QuestionsInline]
    list_display = ("name", "period", "date_start", "date_end", "status", "display", "created_at")
    search_fields = ("name",)
    search_help_text = "ابحث بـ : العنوان"

    list_filter = ("display", "created_at", "date_start", "date_end")
    list_editable = ("display",)
    readonly_fields = ("status","slug",)
    empty_value_display = 'فارغ'
    list_per_page = 15
    
    def status(self, obj):
        from datetime import datetime
        today = datetime.today()
        if obj.date_end:
            if obj.date_end >= today.date():return format_html("<span style='color:#00ff4e;'>نشط</apan>") 
            else:return format_html("<span style='color:#f00;'>منتهي</apan>")
    status.short_description = "الحالة"


class CustomPoints(admin.ModelAdmin):
    list_display = ("user", "quiz", "answer", "proints")
    search_fields = ("correct_answer_point__correct_answer__question__quiz__name", "correct_answer_point__created_by__name",)
    search_help_text = "ابحث بـ : النموذج، اسم المستخدم"
    list_display_links = ("proints",)
    list_per_page = 15
    def user(self, obj):
        return obj.correct_answer_point.created_by
    user.short_description = "اسم المستخدم"
    
    def quiz(self, obj):
        return obj.correct_answer_point.correct_answer.question.quiz
    quiz.short_description = "النموذج"
    
    def answer(self, obj):
        return obj.correct_answer_point.correct_answer
    answer.short_description = " جواب المستخدم"


class CustomPeriod(admin.ModelAdmin):
    list_display = ("name", "status", "date_start", "date_end", "display")
    list_filter = ("date_start", "date_end", "display")
    search_fields = ("name",)
    search_help_text = "ابحث بـ : اسم الفترة"

    def status(self, obj):
        from datetime import datetime
        today = datetime.today()
        if obj.date_end >= today.date():return format_html("<span style='color:#00ff4e;'>نشط</apan>") 
        else:return format_html("<span style='color:#f00;'>انتهى</apan>")
    status.short_description = "الحالة"

    def save_model(self, request, obj, form, change):
        from datetime import datetime
        today = datetime.today()
        if obj.date_start == today.date() or obj.date_start <= today.date():
            if not obj.date_end <= today.date():
                super(CustomPeriod, self).save_model(request, obj, form, change)
            else:
                obj.display = False
                super(CustomPeriod, self).save_model(request, obj, form, change)
        else:
            obj.display = False
            super(CustomPeriod, self).save_model(request, obj, form, change)
admin.site.register(Answers, CustomAnswers)
admin.site.register(Questions, CustomQuestions)
admin.site.register(CorrectAnswer, CustomCorrectAnswer)
admin.site.register(Quiz, CustomQuiz)
admin.site.register(Points, CustomPoints)
admin.site.register(Period, CustomPeriod)

