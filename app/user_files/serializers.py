from rest_framework import serializers

from core.models import Tag, File_type


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag object"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_Fields = ('id',)

class File_typeSerializer(serializers.ModelSerializer):
    """serailizer for file_type objects"""

    class Meta:
        model = File_type
        fields = ('id', 'type')
        read_only_Fields = ('id')
