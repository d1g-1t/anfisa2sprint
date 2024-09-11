from django.shortcuts import render


def description(request):
    """
    Представление для отображения страницы описания.

    Аргументы:
    request -- объект запроса

    Возвращает:
    HTTP-ответ с отрендеренным шаблоном 'about/description.html'
    """
    template = 'about/description.html'
    return render(request, template)