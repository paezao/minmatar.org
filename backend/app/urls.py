"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from ninja import NinjaAPI

from applications.router import router as applications_router
from authentication import UnauthorizedError
from discord.views import discord_login
from eveonline.routers import router
from groups.router import router as groups_router
from groups.router_sigs import router as sigs_router
from groups.router_teams import router as teams_router
from users.router import router as users_router

api = NinjaAPI(title="Minmatar Fleet API", version="1.0.0")
api.add_router("users/", users_router)
api.add_router("eveonline/", router)
api.add_router("groups/", groups_router)
api.add_router("teams/", teams_router)
api.add_router("sigs/", sigs_router)
api.add_router("applications/", applications_router)


@api.exception_handler(UnauthorizedError)
def unauthorized(request, exc):
    return api.create_response(request, {"detail": str(exc)}, status=401)


urlpatterns = [
    path("", RedirectView.as_view(url="api/docs")),
    path("api/", api.urls),
    path("admin/login/", discord_login, name="discord_login_override"),
    path(
        "admin/login/?next=/admin/",
        discord_login,
        name="discord_login_override_2",
    ),
    path("admin/", admin.site.urls),
    path("sso/", include("esi.urls")),
    path("oauth2/", include("discord.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
