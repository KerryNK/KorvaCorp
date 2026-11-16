from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
]

handler404 = "core.views.page_not_found"
handler500 = "core.views.server_error"
