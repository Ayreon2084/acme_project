# Добавьте новые строчки с импортами классов для создания пользователей.
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView


# Импортируем настройки проекта.
from django.conf import settings
# Импортируем функцию, позволяющую серверу разработки отдавать файлы.
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse_lazy


# 1. FBV. 
urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    # Подключаем urls.py приложения для работы с пользователями.
    path('auth/', include('django.contrib.auth.urls')),
    # 1) Чтобы подключить CBV CreateView, есть знакомый путь: 
    # - в файле views.py создать собственный класс, унаследовав его от CreateView,
    # - передать в него имя шаблона, формы и адрес редиректа,
    # - вызвать этот класс в маршрутизаторе с помощью метода as_view().
    # 2) Но есть другой подход: вызвать класс CreateView можно прямо в файле urls.py, 
    # а все нужные атрибуты передать аргументами в метод as_view().
    # В проекте нет отдельного приложения для работы с пользователями, 
    # и разместить CBV некуда; 
    # создавать приложение ради единственного view-класса не хочется. 
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('pages:homepage'),
        ),
        name='registration',
    ),
    path('birthday/', include('birthday.urls')),
    # В конце добавляем к списку вызов функции static.
    # Работает только при DEBUG = True.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Адрес view-функции с ошибкой 404 хранится в переменной handler404 
# (по умолчанию это view-функция django.views.defaults.page_not_found). 
# Также есть handler400, handler403, handler500
handler404 = 'core.views.page_not_found'