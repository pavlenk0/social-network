from django.conf.urls import include, url
from django.contrib import admin
from rest_auth.registration.views import VerifyEmailView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from accounts.api.views import CreateUserView
from pages.api.views import (
    PostCreateAPIView,
    PostLikeAPIView,
    PostListAPIView,
    PostRetrieveAPIView,
    PostUpdateDestroyAPIView
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/account/verify-email/$', VerifyEmailView.as_view(),
        name='rest_verify_email'),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api/auth/refresh-token/', refresh_jwt_token),
    url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^api/auth/registration/$', CreateUserView.as_view(),
        name='user-registration'),
    url(r'^api/auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api/posts/$', PostListAPIView.as_view(), name='posts-list'),
    url(r'^api/post/create/$', PostCreateAPIView.as_view(),
        name='post-create'),
    url(r'^api/post/(?P<pk>[0-9]+)/retrieve/$', PostRetrieveAPIView.as_view(),
        name='post-retrieve'),
    url(r'^api/post/(?P<pk>[0-9]+)/update/$',
        PostUpdateDestroyAPIView.as_view(), name='post-update-delete'),
    url(r'^api/post/(?P<pk>[0-9]+)/like/$', PostLikeAPIView.as_view(),
        name='post-like')

]
