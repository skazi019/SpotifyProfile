from django.urls import path
from .views import (
    get_album,
    get_track,
    login,
    spotify_callback,
    user_profile,
    logout,
    top_tracks_page,
    top_artists_page,
    recent_tracks_page,
)

urlpatterns = [
    path("", login, name="login"),
    path("spotify_callback/", spotify_callback, name="spotify_callback"),
    path("profile/", user_profile, name="user_profile"),
    path("top_tracks/", top_tracks_page, name="top_tracks"),
    path("top_artists/", top_artists_page, name="top_artists"),
    path("recent_tracks/", recent_tracks_page, name="recent_tracks"),
    path("get_album/<str:id>/", get_album, name="get_album"),
    path("get_track/<str:id>/", get_track, name="get_track"),
    path("logout/", logout, name="logout"),
]
