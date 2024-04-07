from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("user.urls")),
    path("api/core/", include("core.urls")),
    path("api/chat/", include("chat.urls")),
    path("api/posts/", include("post.urls")),
    path("api/search/", include("search.urls")),
    path("api/notification/", include("notification.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
