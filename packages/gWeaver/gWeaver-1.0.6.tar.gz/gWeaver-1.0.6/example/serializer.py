from rest_framework import serializers

class serviceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=15, required=False)
    description = serializers.CharField(max_length=15, required=False)
    function = serializers.CharField(max_length=15, required=False)
    criteria = serializers.CharField(max_length=15, required=False)
    