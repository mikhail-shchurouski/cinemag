from django.shortcuts import render
from django.views.generic.base import View

from .models import Movie


class MoviesView(View):
    """
    Класс для отображения списка фильмов на главной.
    """
    def get(self, request):              # request это вся информация присланная в метод из браузера
        movies = Movie.objects.all()     # из базы данных берем все записи из таблицы movies
        return render(request, "cinema/movies.html", {"movies_list": movies})  # рендерим наши фильмы




