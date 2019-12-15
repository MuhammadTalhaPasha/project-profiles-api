from rest_framework import serializers

from core.models import Tag, File_type, User_File


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
        read_only_Fields = ('id',)

class User_FileSerializer(serializers.ModelSerializer):
    """serialize uesr files"""
    file_types = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=File_type.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = User_File
        fields = (
            'id', 'title',
            'created_on','file_types', 'tags', 'link'
        )
        read_only_Fields = ('id',)

class UserFileDetailSerializer(User_FileSerializer):
    """serialize a user_file detail"""
    file_types = File_typeSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
