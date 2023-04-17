import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.views.generic import DetailView, ListView, TemplateView
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.mail import send_mail
from .models import *
from category.models import *

from competitions.models import Points, Period

from .forms import Contact_Me_Form



from django.contrib.auth import get_user_model
User = get_user_model()

from django.db.models import Case, Value, When

def index(request):
    all_news = ApprovalNews.objects.filter(news__display=True, approval="AP").order_by('-news__created_in')[:3]
    category = Category.objects.filter(display=True)
    users  = User.objects.all()
    data_category = ApprovalData_Category.objects.filter(data_category__display=True, approval="AP").order_by('-data_category__created_in')[:3]
    
    try:
        period = Period.objects.get(display=True)
    except:
        period = None

    li_users  = []
    li_points = []

    for i in users:
        po = Points.objects.filter(correct_answer_point__created_by=i, correct_answer_point__correct_answer__question__quiz__period__display=True ,correct_answer_point__correct_answer__is_correct=True)

        if po:
            li_users.append(str(i.name))
        to_pos = 0
        for p in po:
            to_pos += p.proints
        if to_pos == 0:
            pass
        else:
            li_points.append([to_pos,[i.name]])

    new_li_points = []
    new_li_users  = []

    if not li_points:
        new_li_points = [30,25,20,15,10]
        new_li_users = ["محمد", "خالد", "زياد", "عبد الله", "صالح"]
    else:
        li_points.sort(reverse=True)
        for x in range(0,5):
            new_li_points.append(li_points[x][0])   # show the point
            new_li_users.append(li_points[x][1][0]) # show the name



    # if request.method == 'POST':
    
    #     form = Contact_Me_Form(request.POST)

    #     # check if data from the form is clean
    #     if form.is_valid():
    #         cd = form.cleaned_data

    # else:
    #     form = Contact_Me_Form()
    
    if request.method == "POST":
        form = Contact_Me_Form(request.POST)

        if form.is_valid():    
            form.save()
            return HttpResponseRedirect("/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Contact_Me_Form()

    return render(request , 'index.html' , {
        'all_news' : all_news ,
        'category' : category ,
        'li_users':li_users,
        'li_points':li_points,
        'new_li_users':new_li_users,
        'new_li_points':new_li_points,
        "data_category":data_category,
        "period":period,
        'form':form
    })


def blog_search(request):
    blog_first_5 = ApprovalBlog.objects.filter(blog__display=True, approval="AP").order_by("-blog__created_in")[:5]
    if request.method == "POST":
        search_blog = request.POST['search_blog']
        print(search_blog)
        blogs = ApprovalBlog.objects.filter(blog__title__contains=search_blog, blog__display=True, approval="AP")
        return render(request, 'blog/search_blog.html', {"blogs":blogs, "search_blog":search_blog, "blog_first_5":blog_first_5})
    return render(request , 'blog/search_blog.html')



def blog(request):
    blogs = ApprovalBlog.objects.filter(blog__display=True, approval="AP").order_by("-blog__created_in")
    blog_first_5 = ApprovalBlog.objects.filter(blog__display=True, approval="AP").order_by("-blog__created_in")[:5]

    paginator = Paginator(blogs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        search_blog = request.POST['search_blog']
        blogs = ApprovalBlog.objects.filter(blog__title__contains=search_blog, blog__display=True, approval="AP")
        return render(request, 'blog/blog-right-sidebar.html', {'page_obj': page_obj, "blogs":blogs, "blog_first_5":blog_first_5, "search_blog":search_blog})
    else:
        return render(request , 'blog/blog-right-sidebar.html' , {
            'blog_first_5':blog_first_5,
            'page_obj': page_obj,
        })



def blog_single(request, bl_str):
    blog_first_5 = ApprovalBlog.objects.filter(blog__display=True, approval="AP").order_by("-blog__created_in")[:5]
    blog = get_object_or_404(ApprovalBlog, blog__slug=bl_str, blog__display=True)
    
    if request.method == "POST":
        search_blog = request.POST['search_blog']
        blogs = ApprovalBlog.objects.filter(blog__title__contains=search_blog, blog__display=True, approval="AP")
        return render(request, 'blog/blog-single-post.html', {'blog': blog, "blogs":blogs, "blog_first_5":blog_first_5, "search_blog":search_blog})
    else:
        return render(request , 'blog/blog-single-post.html' , {
            'blog':blog,
            'blog_first_5':blog_first_5,
        })
        


def news(request):
    all_news = ApprovalNews.objects.filter(news__display=True, approval="AP").order_by('-news__created_in')
    news_first_5 = ApprovalNews.objects.filter(news__display=True, approval="AP").order_by("-news__created_in")[:5]
    try:
        news_slide0 = NewsSlide.objects.all()[0]
        news_slide = NewsSlide.objects.all()[1:]
    except:
        news_slide0 = None
        news_slide = None

    paginator = Paginator(all_news, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request , 'news.html' , {
        'page_obj' : page_obj ,
        'news_first_5':news_first_5,
        'news_slide0':news_slide0,
        'news_slide':news_slide,
    })


def news_detal(request, slug):
    news = ApprovalNews.objects.get(news__slug=slug, news__display=True, approval="AP")
    
    return render(request , 'news_detail.html' , {
        'news' : news ,
    })


# Errors Func
def handel404(request, exception):
    return render(request, 'errors/404.html')

def handel500(request):
    return render(request, 'errors/500.html')