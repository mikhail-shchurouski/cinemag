from django.db import models
from datetime import date
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """
    Категории фильмов.
    """
    name = models.CharField(max_length=150, verbose_name="Категория")
    description = models.TextField(verbose_name="Описание")
    url = models.SlugField(max_length=160, unique=True)

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    @classmethod
    def get_default_pk(cls):
        # метод создает раздел для фильмов у которых не указана категория
        obj, created = cls.objects.get_or_create(name="Нет категории")  # создать если нет раздела
        return obj.pk

    def __str__(self):
        return f'{self.name}'


class ActorDirector(models.Model):
    """
    Актеры и режиссеры учавствующие в сьемках фильма.
    """
    name = models.CharField(max_length=100, verbose_name="Имя")
    age = models.PositiveSmallIntegerField(default=0, verbose_name="Возраст")   # от 0 до 32767
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='actors/', verbose_name="Изображение")

    class Meta:
        verbose_name = _("Актеры и режиссеры")
        verbose_name_plural = _("Актеры и режиссеры")

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    """
    Жанры кино.
    """
    name = models.CharField(max_length=100, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание")
    url = models.SlugField(max_length=160, unique=True)

    class Meta:
        verbose_name = _("Жанр")
        verbose_name_plural = _("Жанры")

    def __str__(self):
        return f'{self.name}'


class Movie(models.Model):
    """
    Фильмы
    """
    title = models.CharField(max_length=100, verbose_name="Название")
    tagline = models.CharField(max_length=100, default="", verbose_name="Слоган")
    description = models.TextField(verbose_name="Описание")
    poster = models.ImageField(upload_to="movies/", verbose_name="Постер")
    year = models.PositiveSmallIntegerField(default=2021, verbose_name="Дата выхода")
    country = models.CharField(max_length=30, verbose_name="Страна")
    directors = models.ManyToManyField(ActorDirector, verbose_name="Режиссер",
                                       related_name="film_director")
    actors = models.ManyToManyField(ActorDirector, verbose_name="Актер",
                                    related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="Жанр")
    world_premiere = models.DateField(default=date.today, verbose_name="Примъера в мире")
    budget = models.PositiveIntegerField(default=0, help_text="$", verbose_name="Бюджет")
    fees_in_usa = models.PositiveIntegerField(default=0, help_text="$", verbose_name="Сборы в США")
    fees_in_world = models.PositiveIntegerField(default=0, help_text="$", verbose_name="Сборы в мире")
    category = models.ForeignKey(Category, verbose_name="Категория",
                                 on_delete=models.SET_DEFAULT,
                                 default=Category.get_default_pk)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField(default=False, verbose_name="Черновик")

    class Meta:
        verbose_name = _("Фильм")
        verbose_name_plural = _("Фильмы")

    def __str__(self):
        return f'{self.title} | {self.year} | {self.genres} | {self.directors}'


class MovieShots(models.Model):
    """
    Кадры из фильма
    """
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="movie_shots/", verbose_name="Изображение")
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Кадр из фильма")
        verbose_name_plural = _("Кадры из фильма")

    def __str__(self):
        return f'{self.pk}|{self.title}|{self.movie}'


class RatingStar(models.Model):
    """
    Звезды рейтинга фильма
    """
    value = models.PositiveSmallIntegerField(default=0, verbose_name="Значение")

    class Meta:
        verbose_name = _("Звезда рейтинга")
        verbose_name_plural = _("Звезды рейтинга")

    def __str__(self):
        return self.value


class Rating(models.Model):
    """
    Рейтинг
    """
    ip = models.CharField(max_length=15, verbose_name="IP адрес")
    stat = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Звезда")
    movie = models.ForeignKey(Movie, on_delete=models.CharField, verbose_name="Фильм")

    class Meta:
        verbose_name = _("Рейтинг")
        verbose_name_plural = _("Рейтинги")

    def __str__(self):
        return f'{self.stat} - {self.movie}'


class Reviews(models.Model):
    """
    Отзывы
    """
    email = models.EmailField()
    name = models.CharField(max_length=100, verbose_name="Имя")
    text = models.TextField(max_length=5000, verbose_name="Сообщение")
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.SET_NULL,
                               null=True, blank=True)
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")

    def __str__(self):
        return f'{self.name}|{self.movie}'
