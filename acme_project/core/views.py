# core/views.py
from django.shortcuts import render


# Кастомная страница 404
def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию; 
    # выводить её в шаблон пользовательской страницы 404 мы не станем.
    return render(request, 'core/404.html', status=404)


# Если при отправке формы не был отправлен csrf-токен — Django вернёт ошибку 403, 
# но страница этой ошибки кастомизируется отдельно. 
# Шаблон и view-функция готовятся так же, как и для других страниц, 
# но переопределяется не хендлер, 
# а константа CSRF_FAILURE_VIEW в settings.py.
def csrf_failure(request, reason=''):
    return render(request, 'core/403csrf.html', status=403)
