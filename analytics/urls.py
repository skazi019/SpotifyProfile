from cmath import log
from django.urls import path
from .views import (
    get_album,
    login,
    spotify_callback,
    user_profile,
    logout,
)

urlpatterns = [
    path("", login, name="login"),
    path("spotify_callback/", spotify_callback, name="spotify_callback"),
    path("profile/", user_profile, name="user_profile"),
    path("album/<str:id>/", get_album, name="album"),
    path("logout/", logout, name="logout"),
]
