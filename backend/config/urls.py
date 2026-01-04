from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from core.health import health_view
from core.metrics import metrics_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_view, name="health"),
    path("metrics/", metrics_view, name="metrics"),
    path("docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("api/auth/", include("auth_app.urls")),
    path("api/", include("example_app.urls")),
]
