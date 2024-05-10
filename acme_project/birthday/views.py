# # Импортируем класс пагинатора.
# from django.core.paginator import Paginator
# # Дополнительно импортируйте шорткат для редиректа.
from django.shortcuts import get_object_or_404, redirect, render
# Импортируем класс ошибки (в данном случае - 403).
from django.core.exceptions import PermissionDenied 
# Для декорирования в FBV
from django.contrib.auth.decorators import login_required
# Для проверки аутентификации в CBV
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.http import HttpResponse

from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy, reverse

# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
from .forms import BirthdayForm, CongratulationForm
# Импортируем модель дней рождения.
from .models import Birthday, Congratulation
# # Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown


# def edit_birthday(request, pk):
#     # Находим запрошенный объект для редактирования по первичному ключу
#     # или возвращаем 404 ошибку, если такого объекта нет.
#     # При поиске объекта дополнительно указываем текущего пользователя.
#     instance = get_object_or_404(Birthday, pk=pk, author=request.user)
#     # Связываем форму с найденным объектом: передаём его в аргумент instance.
#     if instance.author != request.user:
#         # Здесь может быть как вызов ошибки, так и редирект на нужную страницу.
#         raise PermissionDenied 
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

# # 1. Function-Based View (FBV).

# # Тестовая функция для декоратора

# @login_required
# def simple_view(request):
#     return HttpResponse('Страница для тех, кто залогинен!')


# def birthday(request, pk=None):
#     # print(request.GET)  # Получить данные GET-запроса
#     # Если в запросе указан pk (если получен запрос на редактирование объекта):
    # if pk is not None:
    #     # Получаем объект модели или выбрасываем 404 ошибку.
    #     #  Для проверки авторизации в эту функцию добавляется фильтр, 
    #     #  который сравнивает значение поля author модели 
    #     #  с объектом пользователя из запроса.
    #     instance = get_object_or_404(Birthday, pk=pk, author=request.user)
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
#     # Создаём словарь контекс та сразу после инициализации формы.
#     context = {'form': form}
#     # Если данные валидны...
#     # Проверка is_valid выполняется и в шаблоне, и во view-функции. 
#     # В шаблоне проверка предотвращает вывод приветствия, 
#     # если форма содержит ошибки. 
#     # Во view-функции проверка обеспечивает валидность данных, 
#     # которые будут переданы для дальнейшей обработки. 
    # if form.is_valid():
    #     # Проверка авторства в FVB:
    #     # 1. При обработке формы создаётся объект модели Birthday, 
    #     # но не сохраняется в БД (если сохранить его сразу — 
    #     #                         в нём не будет данных об авторе). 
    #     # Создание объекта модели без его сохранения выполняется с помощью
    #     # метода form.save() с аргументом commit=False:
    #     instance = form.save(commit=False)
    #     # 2. После этого полю объекта author присваивается нужное значение:
    #     instance.author = request.user
    #     # 3. Теперь нужно сохранить объект модели в БД: у объектов моделей тоже есть метод save(). 
    #     # Сохранять нужно именно объект модели, а не форму 
    #     # — ведь значение поля author записано именно в объект модели.
    #     instance.save() 


    #     # В классе ModelForm есть встроенный метод save(), 
    #     # он позволяет сохранить данные из формы в БД. 
    #     # После сохранения метод save() возвращает сохранённый объект 
    #     # — это можно использовать для подтверждения, 
    #     # что сохранение данных прошло успешно.
    #     form.save()
    #     # ...вызовем функцию подсчёта дней:
    #     birthday_countdown = calculate_birthday_countdown(
    #         # ...и передаём в неё дату из словаря cleaned_data.
    #         form.cleaned_data['birthday']
    #     )
    #     # Обновляем словарь контекста: добавляем в него новый элемент.
    #     context.update({'birthday_countdown': birthday_countdown})
    # return render(request, 'birthday/birthday.html', context)


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

# # Обработка данных из формы CongratulationForm в виде FBV.
# @login_required
# def add_comment(request, pk):
#     # Получаем объект дня рождения или выбрасываем 404 ошибку.
#     birthday = get_object_or_404(Birthday, pk=pk)
#     # Функция должна обрабатывать только POST-запросы.
#     form = CongratulationForm(request.POST)
#     if form.is_valid():
#         # Создаём объект поздравления, но не сохраняем его в БД.
#         congratulation = form.save(commit=False)
#         # В поле author передаём объект автора поздравления.
#         congratulation.author = request.user
#         # В поле birthday передаём объект дня рождения.
#         congratulation.birthday = birthday
#         # Сохраняем объект в БД.
#         congratulation.save()
#     # Перенаправляем пользователя назад, на страницу дня рождения.
#     return redirect('birthday:detail', pk=pk) 

# # ----------------------------------------------------------------
# # 2. Class-Basev View (CBV).

class CongratulationCreateView(LoginRequiredMixin, CreateView):
    Birthday = None
    model = Congratulation
    form_class = CongratulationForm

    # Переопределяем dispatch()
    def dispatch(self, request, *args, **kwargs):
        self.birthday = get_object_or_404(Birthday, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    # Переопределяем form_valid()
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.birthday = self.birthday
        return super().form_valid(form)

    # Переопределяем get_success_url()
    def get_success_url(self):
        return reverse('birthday:detail', kwargs={'pk': self.birthday.pk})


# Чтобы не проверять авторство во всех CBV, где это требуется,
# проще написать свой миксин, наследуемый от UserPassesTestMixin.
class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


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
# Наследуем BirthdayCreateView от CreateView и от миксина LoginRequiredMixin:
# При этом никаких изменений в маршрут вносить не нужно, он остаётся тем же, что и был:
class BirthdayCreateView(LoginRequiredMixin, CreateView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # # Этот класс сам может создать форму на основе модели!
    # # Нет необходимости отдельно создавать форму через ModelForm.
    # # Указываем поля, которые должны быть в форме:
    # fields = '__all__'  # указывается только в случае отсутствия form_class
    # Указываем имя формы:
    form_class = BirthdayForm

    # Объект пользователя можно получить прямо из запроса, 
    # в котором отправлены данные формы: 
    # объект пользователя, отправившего запрос, 
    # доступен в свойстве request.user. 
    # Остаётся передать объект пользователя в поле объекта формы.
    # Документация сообщает, что присвоить значение нужному полю в CBV 
    # можно через переопределение метода валидации:
    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)

# Класс UserPassesTestMixin унаследован от AccessMixin, 
# который по умолчанию переадресует анонимных пользователей 
# на страницу логина. 
# Поэтому при использовании UserPassesTestMixin миксин LoginRequiredMixin можно не использовать:
# он будет избыточным.
# Такую проверку надо разместить во всех CBV, где нужна проверка авторства. Выглядит громоздко: помимо того, что при объявлении CBV надо добавить миксин UserPassesTestMixin, в каждый класс придётся добавлять одно и то же описание метода test_func(). 


# Такую проверку надо разместить во всех CBV, где нужна проверка авторства.
# Выглядит громоздко: помимо того, что при объявлении CBV надо 
# добавить миксин UserPassesTestMixin, 
# в каждый класс придётся добавлять одно и то же описание метода test_func(). 
# В такой ситуации гораздо выгоднее написать собственный миксин, 
# унаследованный от UserPassesTestMixin:
# Добавляем миксин для тестирования пользователей, обращающихся к объекту.
class BirthdayUpdateView(OnlyAuthorMixin, UpdateView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # # Этот класс сам может создать форму на основе модели!
    # # Нет необходимости отдельно создавать форму через ModelForm.
    # # Указываем поля, которые должны быть в форме:
    # fields = '__all__'  # указывается только в случае отсутствия form_class
    # Указываем имя формы:
    form_class = BirthdayForm

    # Определяем метод test_func() для миксина UserPassesTestMixin:
    def test_func(self):
        # Получаем текущий объект.
        object = self.get_object()
        # Метод вернёт True или False. 
        # Если пользователь - автор объекта, то тест будет пройден.
        # Если нет, то будет вызвана ошибка 403.
        return object.author == self.request.user 


class BirthdayDeleteView(OnlyAuthorMixin, DeleteView):
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
        # Записываем в переменную form пустой объект формы.
        context['form'] = CongratulationForm()
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['congratulations'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.congratulations.select_related('author')
        )
        # Возвращаем словарь контекста.
        return context
