from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage
from rest_framework.response import Response
from rest_framework import status

from appauth.api_authentications import (
    SessionAuthenticationUnsafeMethods,
)

from utils.response_handler import generic_response
from utils.pagination import PaginationKeys

from .models import (
    Post,
)

from .serializers import (
    PostSerializer,
)

from .constants import (
    ResponseKeys,
)


class AllPostsAPI(APIView):
    """
    API to get all posts or to add a new one.

    > NOTE: The user must be logged in to create a new post.
    """
    authentication_classes = (SessionAuthenticationUnsafeMethods, )
    serializer_class = PostSerializer

    def get(self, request):
        """
        An API for fetching all posts in paginated manner.

        **Header**:

            {
                "Content-Type": "application/json"
            }
        """
        page = request.GET.get(PaginationKeys.PAGE, 1)

        posts = Post.objects.all().order_by('-added_on')
        paginator = Paginator(posts, PaginationKeys.ITEMS_PER_PAGE)

        try:
            posts = paginator.page(page)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        serializer = self.serializer_class(posts, many=True)

        context = {
            PaginationKeys.PAGE: page,
            PaginationKeys.COUNT: paginator.num_pages,
            ResponseKeys.POSTS: serializer.data}

        return Response(
            context,
            status=status.HTTP_200_OK)

    def post(self, request):
        """
        An API for creating a post. Only logged in user can create a post.

        **Header**:

            {
                "Content-Type": "application/json"
            }

        **Data**:

            {
                "title": "Hello World",
                "body": "<h2>Hello</h2><p>Some dummy text</p>",
                "category": 1,
                "isActive": true
            }
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        return Response(
            generic_response(ResponseKeys.POST_SAVED))


class PostAPI(APIView):
    """
    An API to get, update or delete a post by its ID.

    > NOTE: The user must be logged in to create, update or delete a post.
    """
    authentication_classes = (SessionAuthenticationUnsafeMethods, )
    serializer_class = PostSerializer

    def get_obj(self, post_id):
        try:
            post = Post.objects.get(id=post_id)
            return post
        except Post.DoesNotExist:
            return None

    def get(self, request, post_id):
        """
        An API for creating a post. Only logged in user can create a post.

        **Header**:

            {
                "Content-Type": "application/json"
            }

        **Data**:

            {
                "title": "Hello World",
                "body": "<h2>Hello</h2><p>Some dummy text</p>",
                "category": 1,
                "isActive": true
            }
        """
        post = self.get_obj(post_id)
        if post:
            serializer = self.serializer_class(post)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK)
        else:
            return Response(
                ResponseKeys.POST_NOT_FOUND,
                status=status.HTTP_404_NOT_FOUND)

    def post(self, request, post_id):
        """
        An API for updating a post. Only logged in user can update a post.

        **Header**:

            {
                "Content-Type": "application/json"
            }

        **Data**:

            {
                "title": "Hello World",
                "body": "<h2>Hello</h2><p>Some dummy text</p>",
                "category": 1,
                "isActive": true
            }
        """
        post = self.get_obj(post_id)
        if post:
            serializer = self.serializer_class(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    generic_response(ResponseKeys.POST_UPDATED),
                    status=status.HTTP_200_OK)
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                ResponseKeys.POST_NOT_FOUND,
                status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, post_id):
        """
        An API for deleting a post. Only logged in user can delete a post.

        **Header**:

            {
                "Content-Type": "application/json"
            }
        """
        post = self.get_obj(post_id)
        if post:
            post.delete()
            return Response(
                generic_response(ResponseKeys.POST_DELETED),
                status=status.HTTP_200_OK)
        else:
            return Response(
                ResponseKeys.POST_NOT_FOUND,
                status=status.HTTP_404_NOT_FOUND)
