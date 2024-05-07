# # Импортируем класс пагинатора.
# from django.core.paginator import Paginator
# # Дополнительно импортируйте шорткат для редиректа.
# from django.shortcuts import get_object_or_404, redirect, render

from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
from .forms import BirthdayForm
# Импортируем модель дней рождения.
from .models import Birthday
# # Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown


# def edit_birthday(request, pk):
#     # Находим запрошенный объект для редактирования по первичному ключу
#     # или возвращаем 404 ошибку, если такого объекта нет.
#     instance = get_object_or_404(Birthday, pk)
#     # Связываем форму с найденным объектом: передаём его в аргумент instance.
#     form = BirthdayForm(request.POST or None, instance=instance)
#     context = {
#         'form': form
#     }
#     # Сохраняем данные, полученные из формы, и отправляем ответ:
#     if form.is_valid():
#         form.save()
#         birthday_countdown = calculate_birthday_countdown(
#             form.cleaned_data['birthday']
#         )
#         context.update({'birthday_countdown': birthday_countdown})
#     return render(request, 'birthday/birthday.html', context)

# 1. Function-Based View (FBV).

# def birthday(request, pk=None):
#     # print(request.GET)  # Получить данные GET-запроса
#     # Если в запросе указан pk (если получен запрос на редактирование объекта):
#     if pk is not None:
#         # Получаем объект модели или выбрасываем 404 ошибку.
#         instance = get_object_or_404(Birthday, pk=pk)
#     # Если в запросе не указан pk
#     # (если получен запрос к странице создания записи):
#     else:
#         # Связывать форму с объектом не нужно, установим значение None.
#         instance = None
#     # Передаём в форму либо данные из запроса, либо None. 
#     # В случае редактирования прикрепляем объект модели.
#     form = BirthdayForm(
#         request.POST or None, 
#         instance=instance,
#         # Файлы, переданные в запросе, указываются отдельно.
#         files=request.FILES or None,
#     )
#     # Если в GET-запросе были переданы параметры — значит, 
#     # объект request.GET не пуст и этот объект передаётся в форму; 
#     # если же объект request.GET пуст — срабатывает условиe or 
#     # и форма создаётся без параметров, через BirthdayForm(None) 
#     # — это идентично обычному BirthdayForm().
#     # Создаём словарь контекста сразу после инициализации формы.
#     context = {'form': form}
#     # Если данные валидны...
#     # Проверка is_valid выполняется и в шаблоне, и во view-функции. 
#     # В шаблоне проверка предотвращает вывод приветствия, 
#     # если форма содержит ошибки. 
#     # Во view-функции проверка обеспечивает валидность данных, 
#     # которые будут переданы для дальнейшей обработки. 
#     if form.is_valid():
#         # В классе ModelForm есть встроенный метод save(), 
#         # он позволяет сохранить данные из формы в БД. 
#         # После сохранения метод save() возвращает сохранённый объект 
#         # — это можно использовать для подтверждения, 
#         # что сохранение данных прошло успешно.
#         form.save()
#         # ...вызовем функцию подсчёта дней:
#         birthday_countdown = calculate_birthday_countdown(
#             # ...и передаём в неё дату из словаря cleaned_data.
#             form.cleaned_data['birthday']
#         )
#         # Обновляем словарь контекста: добавляем в него новый элемент.
#         context.update({'birthday_countdown': birthday_countdown})
#     return render(request, 'birthday/birthday.html', context)


# def delete_birthday(request, pk):
#     # Получаем объект модели или выбрасываем 404 ошибку.
#     instance = get_object_or_404(Birthday, pk=pk)
#     # В форму передаём только объект модели;
#     # передавать в форму параметры запроса не нужно.
#     form = BirthdayForm(instance=instance)
#     context = {
#         'form': form
#     }
#     # Если был получен POST-запрос...
#     if request.method == 'POST':
#         # ...удаляем объект:
#         instance.delete()
#         # ...и переадресовываем пользователя на страницу со списком записей.
#         return redirect('birthday:list')
#     # Если был получен GET-запрос — отображаем форму.
#     return render(request, 'birthday/birthday.html', context)


# def birthday_list(request):
#     # Получаем список всех объектов с сортировкой по id.
#     birthdays = Birthday.objects.order_by('id')
#     # Создаём объект пагинатора с количеством 10 записей на страницу.
#     paginator = Paginator(birthdays, 10)
#     # Получаем из запроса значение параметра page.
#     page_number = request.GET.get('page')
#     # Получаем запрошенную страницу пагинатора. 
#     # Если параметра page нет в запросе или его значение не приводится к числу,
#     # вернётся первая страница.
#     page_obj = paginator.get_page(page_number)
#     # Вместо полного списка объектов передаём в контекст 
#     # объект страницы пагинатора
#     context = {'page_obj': page_obj}
#     return render(request, 'birthday/birthday_list.html', context)


# # ----------------------------------------------------------------
# # 2. Class-Basev View (CBV).


class BirthdayListView(ListView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = 'id'
    # ...и даже настройки пагинации:
    paginate_by = 10


# # Создаём миксин (для отсутствия дублирования атрибутов и методов).
# class BirthdayMixin:
#     # Указываем модель, с которой работает CBV...
#     model = Birthday
#     # Указываем namespace:name страницы, куда будет перенаправлен пользователь
#     # после создания объекта:
#     success_url = reverse_lazy('birthday:list')
# # # Явным образом указываем шаблон.
# # # Можно не указывать если название шаблона: имя_модели_form.html,
# # # то есть в нашем случае 'birthday_form.html', а у нас 'birthday.html'
# # template_name = 'birthday/birthday.html'


# Добавляем миксин первым по списку родительских классов.
class BirthdayCreateView(CreateView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # # Этот класс сам может создать форму на основе модели!
    # # Нет необходимости отдельно создавать форму через ModelForm.
    # # Указываем поля, которые должны быть в форме:
    # fields = '__all__'  # указывается только в случае отсутствия form_class
    # Указываем имя формы:
    form_class = BirthdayForm


class BirthdayUpdateView(UpdateView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # # Этот класс сам может создать форму на основе модели!
    # # Нет необходимости отдельно создавать форму через ModelForm.
    # # Указываем поля, которые должны быть в форме:
    # fields = '__all__'  # указывается только в случае отсутствия form_class
    # Указываем имя формы:
    form_class = BirthdayForm


class BirthdayDeleteView(DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Возвращаем словарь контекста.
        return context
