from django.conf.urls import url

from .views import (
    AllPostsView,
    PostView,
)

urlpatterns = [
    url(r'^all/$', AllPostsView.as_view(), name='all_posts'),
    url(r'^(?P<post_id>[0-9]+)/$', PostView.as_view(), name='post'),
]
