from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from him.app import views

router = routers.DefaultRouter()
router.register(r"person", views.PersonViewSet)

urlpatterns = [
    # Login browsable API Doc
    path('api-auth/', include('rest_framework.urls')),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("bot/like/", views.bot_like_profiles, name="bot_like_profiles"),
    path("bot/send-first-messages/", views.bot_send_first_messages, name="bot_send_first_messages"),
    path("bot/chat-with-matches/", views.bot_chat_with_matches, name="bot_chat_with_matches"),
    path("", include(router.urls)),
]

urlpatterns += staticfiles_urlpatterns()
