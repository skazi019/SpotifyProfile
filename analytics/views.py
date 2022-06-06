import datetime
import requests
import json
import os
from django.shortcuts import render, redirect

# from .credentials import CLIENT_ID, REDIRECT_URI, RESPONSE_TYPE, SCOPE, CLIENT_SECRET
from dotenv import load_dotenv

print(f"Current fiel path: {os.path.dirname(__file__)}")
dotenv_path = os.path.join("../", ".env")
load_dotenv(dotenv_path=dotenv_path)


def login(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
        request.session.set_expiry(3600)  # setting expiry to 5 mins
    else:
        return redirect("user_profile")

    login_url = (
        requests.Request(
            "GET",
            "https://accounts.spotify.com/authorize",
            params={
                "client_id": os.environ.get("CLIENT_ID"),
                "response_type": os.environ.get("RESPONSE_TYPE"),
                "redirect_uri": os.environ.get("REDIRECT_URI"),
                "scope": os.environ.get("SCOPE"),
            },
        )
        .prepare()
        .url
    )
    return render(request, "login.html", {"login_url": login_url})


def spotify_callback(request):
    code = request.GET.get("code")
    error = request.GET.get("error")

    if error == "access_denied":
        return render(request, "failed_login.html")

    token_url = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": os.environ.get("REDIRECT_URI"),
            "client_id": os.environ.get("CLIENT_ID"),
            "client_secret": os.environ.get("CLIENT_SECRET"),
        },
    ).json()

    access_token = token_url["access_token"]
    token_type = token_url["token_type"]
    expires_in = token_url["expires_in"]
    refresh_token = token_url["refresh_token"]

    if request.session.session_key is None:
        request.session.flush()
        return redirect("login")

    request.session["user_data"] = get_user_profile_data(access_token=access_token)

    artists_data = get_top_artists(access_token=access_token)
    request.session["top_artists_short"] = artists_data[0]
    request.session["top_artists_medium"] = artists_data[1]
    request.session["top_artists_long"] = artists_data[2]

    tracks_data = get_top_tracks(access_token=access_token)
    request.session["top_tracks_short"] = tracks_data[0]
    request.session["top_tracks_medium"] = tracks_data[1]
    request.session["top_tracks_long"] = tracks_data[2]

    request.session["recent_tracks"] = json.loads(
        requests.get(
            f"https://api.spotify.com/v1/me/player/recently-played?limit=30",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        ).text
    )["items"]

    return redirect("user_profile")


def get_user_profile_data(access_token):
    userProfile = requests.get(
        "https://api.spotify.com/v1/me",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(access_token),
        },
    )

    userProfile = json.loads(userProfile.text)
    context = {
        "name": userProfile["display_name"],
        "email": userProfile["email"],
        "followers": userProfile["followers"]["total"],
        "spotify_page": userProfile["external_urls"]["spotify"],
        "id": userProfile["id"],
        "profileimage": userProfile["images"][0]["url"],
        "product": userProfile["product"],
        "type": userProfile["type"],
    }
    return context


def get_top_artists(access_token, limit=20):
    top_artists_short = json.loads(
        requests.get(
            f"https://api.spotify.com/v1/me/top/artists?time_range=short_term&limit={limit}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        ).text
    )
    top_artists_medium = json.loads(
        requests.get(
            f"https://api.spotify.com/v1/me/top/artists?time_range=medium_term&limit={limit}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        ).text
    )
    top_artists_long = json.loads(
        requests.get(
            f"https://api.spotify.com/v1/me/top/artists?time_range=long_term&limit={limit}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        ).text
    )

    return [top_artists_short, top_artists_medium, top_artists_long]


def get_top_tracks(access_token, limit=20):
    top_tracks_short = json.loads(
        requests.get(
            f"https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit={limit}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        ).text
    )
    top_tracks_medium = json.loads(
        requests.get(
            f"https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit={limit}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        ).text
    )
    top_tracks_long = json.loads(
        requests.get(
            f"https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit={limit}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        ).text
    )

    return [top_tracks_short, top_tracks_medium, top_tracks_long]


def user_profile(request):
    if not request.session.exists(request.session.session_key):
        return redirect("login")

    try:
        if not (
            request.session.get("user_data")
            and request.session.get("top_artists_short")
            and request.session.get("top_tracks_short")
        ):
            print("Data not found in request")
            request.session.flush()
            return redirect("login")
    except Exception as e:
        request.session.flush()
        return redirect("login")

    user_data = request.session.get("user_data")
    artists_data = request.session.get("top_artists_long")["items"][:10]
    track_data = request.session.get("top_tracks_long")["items"][:10]

    return render(
        request,
        "home.html",
        {
            "user_data": user_data,
            "artists_data": artists_data,
            "track_data": track_data,
        },
    )


def artist_page(request):
    if not request.session.exists(request.session.session_key):
        return redirect("login")

    try:
        if not (
            request.session.get("user_data")
            and request.session.get("top_artists_short")
            and request.session.get("top_tracks_short")
        ):
            print("Data not found in request")
            request.session.flush()
            return redirect("login")
    except Exception as e:
        request.session.flush()
        return redirect("login")

    artists_data_long = request.session.get("top_artists_long")["items"]
    artists_data_medium = request.session.get("top_artists_medium")["items"]
    artists_data_short = request.session.get("top_artists_short")["items"]
    return render(
        request,
        "artists.html",
        {
            "artists_data_short": artists_data_short,
            "artists_data_medium": artists_data_medium,
            "artists_data_long": artists_data_long,
        },
    )


def track_page(request):
    if not request.session.exists(request.session.session_key):
        return redirect("login")
    try:
        token = SpotifyTokens.objects.get(sesssionkey=request.session.session_key)
    except SpotifyTokens.DoesNotExist:
        request.session.flush()
        return redirect("login")

    tracks_data_long = token.top_tracks_long["items"]
    tracks_data_medium = token.top_tracks_medium["items"]
    tracks_data_short = token.top_tracks_short["items"]
    return render(
        request,
        "tracks.html",
        {
            "tracks_data_short": tracks_data_short,
            "tracks_data_medium": tracks_data_medium,
            "tracks_data_long": tracks_data_long,
        },
    )


def recent_page(request):
    if not request.session.exists(request.session.session_key):
        return redirect("login")
    try:
        token = SpotifyTokens.objects.get(sesssionkey=request.session.session_key)
        access_token = token.access_token
    except SpotifyTokens.DoesNotExist:
        request.session.flush()
        return redirect("login")

    recent_tracks = json.loads(
        requests.get(
            f"https://api.spotify.com/v1/me/player/recently-played?limit=30",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        ).text
    )["items"]

    return render(request, "recent_tracks.html", {"recent_tracks": recent_tracks})


def get_album(request, id):
    if not request.session.exists(request.session.session_key):
        return redirect("login")
    try:
        token = SpotifyTokens.objects.get(sesssionkey=request.session.session_key)
        access_token = token.access_token
    except SpotifyTokens.DoesNotExist:
        request.session.flush()
        return redirect("login")

    albumData = json.loads(
        requests.get(
            f"https://api.spotify.com/v1/albums/{id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        ).text
    )

    return render(request, "album.html", {"albumData": albumData})
