from django.conf.urls import url

from .api_views import (
    AllPostsAPI,
    PostAPI,
)

urlpatterns = [
    url(r'^all/$', AllPostsAPI.as_view(), name='all_posts'),
    url(r'^(?P<post_id>[0-9]+)/$', PostAPI.as_view(), name='post'),
]
