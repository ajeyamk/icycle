from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.http import Http404

from .models import (
    Post,
)

from .constants import (
    ResponseKeys,
)

from utils.pagination import PaginationKeys


class AllPostsView(View):
    """
    A view for getting all posts.
    """
    template_name = 'posts/all_posts.html'

    def get(self, request):
        """
        A view to get all the posts.
        """
        page = request.GET.get(PaginationKeys.PAGE, 1)

        posts = Post.objects.all().order_by('-added_on')
        paginator = Paginator(posts, PaginationKeys.ITEMS_PER_PAGE)

        try:
            posts = paginator.page(page)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {
            ResponseKeys.POSTS: posts}
        return render(request, self.template_name, context)


class PostView(View):
    """
    A view to get a post.
    """
    template_name = 'posts/post.html'

    def get(self, request, post_id):
        """
        A view to get a post by its id.
        """
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise Http404
        context = {
            ResponseKeys.POST: post}
        return render(request, self.template_name, context)
