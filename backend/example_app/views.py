from rest_framework.viewsets import ModelViewSet

from example_app.models import ExampleItem
from example_app.serializers import ExampleItemSerializer


class ExampleItemViewSet(ModelViewSet):
    queryset = ExampleItem.objects.all().order_by("id")
    serializer_class = ExampleItemSerializer
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fields = ["id", "name", "created_at", "updated_at"]
    ordering = ["id"]
