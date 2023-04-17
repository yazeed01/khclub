from django.shortcuts import render
from django.core.paginator import Paginator

from .models import *


def data_category(request , slug):
    category = Category.objects.get(slug=slug)
    data_category = ApprovalData_Category.objects.filter(data_category__category__slug=slug, data_category__display=True, approval="AP").order_by("-data_category__created_in")
    
    paginator = Paginator(data_category, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request , 'data_category.html' , {
        'page_obj' : page_obj,
        'category' : category,
    })