from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms-of-use/", views.terms_of_use, name="terms_of_use"),
]

handler404 = "core.views.page_not_found"
handler500 = "core.views.server_error"
