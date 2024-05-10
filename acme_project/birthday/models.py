# birthday/models.py

from django.contrib.auth import get_user_model

from django.db import models
# Импортируем функцию reverse() для получения ссылки на объект.
from django.urls import reverse

# # Импортируем функцию-валидатор (для форм на основе forms.ModelForm).
from .validators import real_age

# Да, именно так всегда и ссылаемся на модель пользователя!
User = get_user_model()


class Birthday(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField(
        'Фамилия', blank=True, help_text='Необязательное поле', max_length=20
    )
    birthday = models.DateField(
        'Дата рождения',
        # Если валидатор привязан к модели —
        # валидация будет срабатывать и при управлении данными
        # через формы в админке:
        validators=(real_age,)
    )
    # Директория для загрузки файлов из конкретного поля задаётся 
    # в классе ImageField в аргументе upload_to. 
    # Директория с таким названием будет создана в папке, 
    # указанной в настройках MEDIA_ROOT. 
    image = models.ImageField('Фото', upload_to='birthdays_images', blank=True)
    author = models.ForeignKey(
        User, verbose_name='Автор записи', on_delete=models.CASCADE, null=True
    )

    # Добавим к модели Birthday проверку на уникальность записи: 
    # совокупность значений полей «Имя», «Фамилия» и «Дата рождения» 
    # не должна повторяться в БД. 
    # Подобные проверки настраиваются с помощью атрибута constraints 
    # (англ. «ограничения») подкласса Meta, 
    # где указывается класс model.UniqueConstraint 
    # (ограничение на уникальность). 
    class Meta:
        constraints = (
            # В этом классе указывается
            models.UniqueConstraint(
                # - перечень полей, совокупность которых должна быть уникальна;
                fields=('first_name', 'last_name', 'birthday'),
                # - имя ограничения.
                name='Unique person constraint',
            ),
        )

    def get_absolute_url(self):
        # С помощью функции reverse() возвращаем URL объекта.
        return reverse("birthday:detail", kwargs={"pk": self.pk})


class Congratulation(models.Model):
    text = models.TextField('Текст поздравления')
    birthday = models.ForeignKey(
        Birthday,
        on_delete=models.CASCADE,
        related_name='congratulations',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('created_at',)




