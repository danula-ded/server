from rest_framework.viewsets import ModelViewSet

from example_app.models import ExampleItem
from example_app.serializers import ExampleItemSerializer


class ExampleItemViewSet(ModelViewSet):
    queryset = ExampleItem.objects.all().order_by("id")
    serializer_class = ExampleItemSerializer
