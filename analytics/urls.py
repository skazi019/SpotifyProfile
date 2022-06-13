from django.urls import path
from .views import (
    get_album,
    get_track,
    get_artist,
    login,
    spotify_callback,
    user_profile,
    logout,
    top_tracks_page,
    top_artists_page,
    recent_tracks_page,
    user_followed_artists,
    all_playlists,
    get_playlist,
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
    path("get_artist/<str:id>/", get_artist, name="get_artist"),
    path("followed_artists/", user_followed_artists, name="followed_artists"),
    path("all_playlists/", all_playlists, name="all_playlists"),
    path("get_playlist/<str:id>/", get_playlist, name="get_playlist"),
    path("logout/", logout, name="logout"),
]
