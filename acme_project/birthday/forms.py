from django import forms
# Импорт функции для отправки почты.
from django.core.mail import send_mail
# Импортируем класс ошибки валидации.
from django.core.exceptions import ValidationError
# Импортируем класс модели Birthday.
from .models import Birthday
# # Импортируем функцию-валидатор (для форм на основе forms.Form).
# from .validators import real_age

# 1. Вариант форм для случаев без внесений изменений в БД.

# class BirthdayForm(forms.Form):
#     first_name = forms.CharField(label='Имя', max_length=20)
#     last_name = forms.CharField(
#         label='Фамилия',
#         required=False,
#         help_text='Необязательное поле'
#     )
#     birthday = forms.DateField(
#         label='Дата рождения',
#         # Указываем, что виджет для ввода даты должен быть с типом date.
#         widget=forms.DateInput(attrs={'type': 'date'})
        # В аргументе validators указываем список или кортеж 
        # валидаторов этого поля (валидаторов может быть несколько).
        # validators=(real_age,),
#     ) 
# # --------------------------------------------------------
# 2. Вариант форм на основе моделей с внесениями изменений с БД.

# Множество с именами участников Ливерпульской четвёрки.
BEATLES = {'Джон Леннон', 'Пол Маккартни', 'Джордж Харрисон', 'Ринго Старр'}


# Для использования формы с моделями меняем класс на forms.ModelForm.
class BirthdayForm(forms.ModelForm):
    # Удаляем все описания полей.

    # Все настройки задаём в подклассе Meta.
    class Meta:
        # Указываем модель, на основе которой должна строиться форма.
        model = Birthday
        # Указываем, что надо отобразить все поля.
        fields = '__all__'
        # Виджеты указываются в Meta:
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_first_name(self):
        # Получаем значение имени из словаря очищенных данных (Жан Люк).
        first_name = self.cleaned_data['first_name']
        # Разбиваем полученную строку по пробелам 
        # и возвращаем только первое имя (Жан).
        return first_name.split()[0]

    def clean(self):
        # Вызов родительского метода clean (из models -> uniqueconstraints).
        super().clean()
        # Получаем имя и фамилию из очищенных полей формы.
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        # Проверяем вхождение сочетания имени и фамилии во множество имён.
        if f'{first_name} {last_name}' in BEATLES:
            # Отправляем письмо, если кто-то представляется 
            # именем одного из участников Beatles.
            send_mail(
                subject='Another Beatles member',
                message=f'{first_name} {last_name} пытался опубликовать запись!',
                from_email='birthday_form@acme.not',
                recipient_list=['admin@acme.not'],
                fail_silently=True,
            )
            raise ValidationError(
                'Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!'
            )

