from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    from_landing = request.GET.get('from-landing')
    counter_click[from_landing] += 1
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    test_arg = request.GET.get('ab-test-arg', 'original')
    if test_arg == 'original':
        template_name = 'landing.html'
    else:
        template_name = 'landing_alternate.html'
    counter_show[template_name] += 1
    return render(request, template_name)

def conversion(test_arg, template_name):
    try:
        conversion_result = counter_click[test_arg]/counter_show[template_name]
    except ZeroDivisionError:
        conversion_result = 'Не было просмотров.'
    return conversion_result

def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    test_conversion = conversion('test', 'landing_alternate.html')
    original_conversion = conversion('original', 'landing.html')
    return render(request, 'stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
