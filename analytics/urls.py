from django.urls import path
from .views import (
    artist_page,
    get_album,
    login,
    recent_page,
    spotify_callback,
    track_page,
    user_profile,
)

urlpatterns = [
    path("", login, name="login"),
    path("spotify_callback/", spotify_callback, name="spotify_callback"),
    path("profile", user_profile, name="user_profile"),
    path("artists", artist_page, name="artists"),
    path("tracks", track_page, name="tracks"),
    path("album/<str:id>", get_album, name="album"),
    path("recent-tracks", recent_page, name="recent_tracks"),
]
