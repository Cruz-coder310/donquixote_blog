from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap

from chronicles.sitemaps import PostSitemap

# This view helps me to check LOGOUT_REDIRECT_URL setting
from django.shortcuts import render


def home(request):
    return render(request, "home.html", {})


sitemaps = {"posts": PostSitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("chronicles/", include("chronicles.urls")),
    path("accounts/", include("accounts.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
