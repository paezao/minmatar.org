from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests

# Create your views here.

auth_url_discord = f"https://discord.com/api/oauth2/authorize?client_id={settings.DISCORD_CLIENT_ID}&redirect_uri={settings.DISCORD_REDIRECT_URL}&response_type=code&scope=identify"


def home(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"msg": "Hello World"})


def get_authenticated_user(request: HttpRequest):
    print(request.user)
    user = request.user
    return JsonResponse(
        {
            "id": user.id,
            "username": user.username,
            "discord_id": user.discord_user.id,
            "discord_tag": user.discord_user.discord_tag,
            "avatar": user.discord_user.avatar,
        }
    )


def discord_login(request: HttpRequest):
    return redirect(auth_url_discord)


def discord_login_redirect(request: HttpRequest):
    from django.contrib.auth.models import User
    from .models import DiscordUser

    code = request.GET.get("code")
    print(code)
    user = exchange_code(code)

    if DiscordUser.objects.filter(id=user["id"]).exists():
        print("User was found. Logging in...")
        discord_user = DiscordUser.objects.get(id=user["id"])
        discord_user.discord_tag = (
            user["username"] + "#" + user["discriminator"]
        )
        discord_user.avatar = user["avatar"]
        discord_user.save()

        django_user = User.objects.get(username=discord_user.user.username)
        django_user.username = user["username"]
        django_user.save()

        login(request, django_user)

        return redirect("/auth/user")

    django_user = User.objects.create(username=user["username"])
    django_user.username = user["username"]
    django_user.save()

    discord_user = DiscordUser.objects.create(
        user=django_user,
        id=user["id"],
        discord_tag=user["username"] + "#" + user["discriminator"],
        avatar=user["avatar"],
    )

    login(request, django_user)
    return redirect("/auth/user")


def exchange_code(code: str):
    data = {
        "client_id": settings.DISCORD_CLIENT_ID,
        "client_secret": settings.DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.DISCORD_REDIRECT_URL,
        "scope": "identify",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(
        "https://discord.com/api/oauth2/token", data=data, headers=headers
    )
    print(response)
    credentials = response.json()
    access_token = credentials["access_token"]
    response = requests.get(
        "https://discord.com/api/v6/users/@me",
        headers={"Authorization": "Bearer %s" % access_token},
    )
    print(response)
    user = response.json()
    print(user)
    return user
