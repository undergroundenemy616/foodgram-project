from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.flatpages import views
from django.conf.urls import handler404, handler500

urlpatterns = [
    path("", include("main.urls")),
    path("about/", include("django.contrib.flatpages.urls")),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
]

urlpatterns += [
        path("about-us/", views.flatpage, {"url": "/contacts/"}, name="contacts"),
        path("tech/", views.flatpage, {"url": "/tech/"}, name="tech"),
]

handler404 = "main.views.page_not_found"
handler500 = "main.views.server_error"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
