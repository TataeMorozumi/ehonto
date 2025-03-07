from django.urls import path
from . import views
from .views import add_book

urlpatterns = [
    path('favorite/', views.favorite, name='favorite'),
    path('review/', views.review, name='review'),
    path('more_read/', views.more_read, name='more_read'),
    path('settings/', views.settings, name='settings'),
    path('family_invite/', views.family_invite, name='family_invite'),
    path('add/', add_book, name='add_book')
]
