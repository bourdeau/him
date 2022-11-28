from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from rest_framework import routers

from him.app import views

router = routers.DefaultRouter()
router.register(r"person", views.PersonViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("bot/", views.BotView.as_view(), name="bot"),
    path("", include(router.urls)),
]

urlpatterns += staticfiles_urlpatterns()
