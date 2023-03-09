from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("♥search♥", views.search, name="search"),
    path("♥new♥", views.new, name="new"),
    path('♥♥random', views.randoms, name="random"),
    path("<str:title>", views.entry, name="entry"),
    
]
