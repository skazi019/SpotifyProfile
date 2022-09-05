# SpotifyProfile

> Autenticate the users at using Spotify's OAuth2.0 and display user's historic data on a responsive dashboard

<br />

## Goal and Objective

<br />

## Instructions
 - Create an account [here](https://developer.spotify.com/dashboard/) and create an app to get the CLIENT_ID, and CLIENT_SECRET to access the APIs. Also, set your callback URL as
 `http://127.0.0.1:8000/user/spotify_callback/`

    **Note** - using localhost would not be permitted hence using the local ip address

 - Install all the dependencies from the `requirements.txt` file

    ```shell
    pip install -r requirements.txt
    ```

 - Make migrations for the databse with the below command
    ```shell
    python manage.py migrate
    ```

 - To run the project type either
     ```shell
    gunicorn spotify_v1.wsi
     ```
 
    to run in production mode or 

    ```shell
    python manage.py runserver
    ```
    to run in development mode

 - In the browser url bar type "http://127.0.0.1:8000/user/"