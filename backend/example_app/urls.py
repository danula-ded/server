from django.urls import include, path
from rest_framework.routers import DefaultRouter

from example_app.views import ExampleItemViewSet

router = DefaultRouter()
router.register("items", ExampleItemViewSet, basename="example-item")

urlpatterns = [
    path("", include(router.urls)),
]
