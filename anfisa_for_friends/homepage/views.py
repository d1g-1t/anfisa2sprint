from django.shortcuts import render


def index(request):
    """
    Представление для отображения главной страницы.

    Аргументы:
    request -- объект запроса

    Возвращает:
    HTTP-ответ с отрендеренным шаблоном 'homepage/index.html'
    """
    template = 'homepage/index.html'
    return render(request, template)
