from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Movie


class MoviesView(ListView):
    """
    Класс для отображения списка фильмов на главной.
    Атрибут template_name не пишем так как наши шаблон назван move_list
    Django автоматом добавляет к имени модели суффикс _ и list при использовании ListView
    """
    model = Movie
    queryset = Movie.objects.all()   # Выводит все фильмы кроме draft=False


class MovieDetailView(DetailView):
    """Класс который выводит полное описание фильма"""
    model = Movie
    slug_field = "url"  # этот атрибут отвечает за то по какому полю будем искать запись по URL

