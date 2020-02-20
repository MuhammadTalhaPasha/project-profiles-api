from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework import viewsets, mixins, status
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
        assigned_only = bool(self.request.query_params.get('assigned_only'))
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(user_file__isnull=False)

        return queryset.filter(user=self.request.user).order_by('-name').distinct()

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
        assigned_only = bool(self.request.query_params.get('assigned_only'))
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(user_file__isnull=False)

        return queryset.filter(user=self.request.user).order_by('-type').distinct()

    def perform_create(self, serializer):
        """create a new file_Type"""
        serializer.save(user=self.request.user)


class User_FileViewSet(viewsets.ModelViewSet):
    """manage user_files in database"""

    serializer_class = serializers.User_FileSerializer
    queryset = User_File.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """convert a list of string ids to a list of integers"""
        # our_string = '1,2,3'
        # our_string_list = ['1','2','3']
        # converting params to Integers
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """retrive the user_files for the authenticated user"""
        tags = self.request.query_params.get('tags')
        file_types = self.request.query_params.get('file_types')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if file_types:
            file_type_ids = self._params_to_ints(file_types)
            queryset = queryset.filter(file_types__id__in=file_type_ids)

        return queryset.filter(user=self.request.user)

        # tags = self.request.query_params.get('tags')
        # file_types = self.request.query_params.get('file_types')
        # queryset = self.queryset
        # if tags:
        #     tag_ids = self._params_to_ints(tags)
        #     #for filtering a ForeignKey id then we do "__" i.e tags__id_in
        #     queryset = queryset.filter(tags__id__in=tag_ids)
        # if file_types:
        #     file_type_ids = self._params_to_ints(file_types)
        #     #for filtering a ForeignKey id then we do "__" i.e tags__id_in
        #     queryset = queryset.filter(file_types__id__in=file_type_ids)
        # return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.UserFileDetailSerializer
        elif self.action == 'upload_file':
            return serializers.UserFile_FilesSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """create a new user user_File"""
        serializer.save(user=self.request.user)

    @action(methods=['POST', 'GET'], detail=True, url_path='upload-file')
    def upload_file(self, request, pk=None):
        """upload an file/image to a userfile"""
        user_file = self.get_object()
        serializer = self.get_serializer(
            user_file,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
