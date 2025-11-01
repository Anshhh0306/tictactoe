from django.contrib import admin
from django.urls import path
from game import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.login_view, name="login"),
    path("game/", views.game_view, name="game"),
    path("logout/", views.logout_view, name="logout"),
]
