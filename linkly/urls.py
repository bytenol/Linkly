from django.urls import path

from . import views

urlpatterns = [
    path("", views.home),
    path("s/<str:t_url>/", views.redirectUrl),
    path("create/", views.addUrl),
]
