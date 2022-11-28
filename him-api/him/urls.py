from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from rest_framework import routers

from him.app import views

router = routers.DefaultRouter()
router.register(r"personn", views.PersonnViewSet)
router.register(r"bot", views.BotViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]

urlpatterns += staticfiles_urlpatterns()
