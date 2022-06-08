from cmath import log
from django.urls import path
from .views import (
    get_album,
    get_track,
    login,
    spotify_callback,
    user_profile,
    logout,
)

urlpatterns = [
    path("", login, name="login"),
    path("spotify_callback/", spotify_callback, name="spotify_callback"),
    path("profile/", user_profile, name="user_profile"),
    path("get_album/<str:id>/", get_album, name="get_album"),
    path("get_track/<str:id>/", get_track, name="get_track"),
    path("logout/", logout, name="logout"),
]
