from django.shortcuts import render


def ice_cream_detail(request, pk):
    """
    Представление для отображения деталей мороженого.

    Аргументы:
    request -- объект запроса
    pk -- первичный ключ мороженого

    Возвращает:
    HTTP-ответ с отрендеренным шаблоном 'ice_cream/detail.html'
    """
    template = 'ice_cream/detail.html'
    context = {}
    return render(request, template, context)


def ice_cream_list(request):
    """
    Представление для отображения списка мороженого.

    Аргументы:
    request -- объект запроса

    Возвращает:
    HTTP-ответ с отрендеренным шаблоном 'ice_cream/list.html'
    """
    template = 'ice_cream/list.html'
    context = {}
    return render(request, template, context)
