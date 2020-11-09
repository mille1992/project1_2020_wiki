from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/createNewEntry", views.createNewEntry, name="createNewEntry"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/edit/<str:entryTitle>", views.editEntry, name="editEntry")
]
