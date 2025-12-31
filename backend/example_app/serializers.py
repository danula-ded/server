from rest_framework import serializers

from example_app.models import ExampleItem


class ExampleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleItem
        fields = ["id", "name", "created_at", "updated_at"]
