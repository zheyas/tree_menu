from .models import Page
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.template import TemplateDoesNotExist

def main(request):
    context = {
        "title": "Главная страница",
        "page_title": "Добро пожаловать в проект Tree Menu",
        "content": "<p>Это демонстрационная страница с универсальным шаблоном.</p>",
    }
    return render(request, 'tree_menu/universal_page.html', context)


def universal_page(request, slug):
    # slug приходит как, например, "about", "info/company" и т.д.
    page_obj = get_object_or_404(Page, slug=slug)
    context = {
        "title": page_obj.title,
        "page_title": page_obj.page_title or page_obj.title,
        "content": page_obj.content,
    }
    return render(request, "tree_menu/universal_page.html", context)
