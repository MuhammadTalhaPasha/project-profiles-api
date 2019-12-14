from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, File_type, User_File

from user_files import serializers

# class BaseFilesAttrViewSet(viewsets.GenericViewSet,
#                            mixins.ListModelMixin,
#                            mixins.CreateModelMixin):
#     """base viewsets for user owned files attributes"""
#     authentication_classes = (TokenAuthentication,)
#     permissions_classes = (IsAuthenticated,)
#
#     def get_queryset(self):
#         """return objects for the current authenticated user only"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')
#
#     def perform_create(self, serializer):
#         """create a new object"""
#         serializer.save(user=self.request.user)


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """create a new tag"""
        serializer.save(user=self.request.user)

class File_typeViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin):
    """manage file_type in the database"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = File_type.objects.all()
    serializer_class = serializers.File_typeSerializer

    def get_queryset(self):
        """return object for the current authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-type').distinct()

    def perform_create(self, serializer):
        """create a new file_Type"""
        serializer.save(user=self.request.user)


class User_FileViewSet(viewsets.ModelViewSet):
    """manage user_files in database"""

    serializer_class = serializers.User_FileSerializer
    queryset = User_File.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """retrive the user_files for the authenticated user"""
        return self.queryset.filter(user=self.request.user)
