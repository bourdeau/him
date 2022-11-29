from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from him.app import views

router = routers.DefaultRouter()
router.register(r"person", views.PersonViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("bot/", views.BotView.as_view(), name="bot"),
    path("health/", views.HealthView.as_view(), name="health"),
    path("", include(router.urls)),
]

urlpatterns += staticfiles_urlpatterns()
