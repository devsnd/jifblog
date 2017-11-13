from django.conf.urls import url
from .views import FeedView, PasswordView, LogoutView

urlpatterns = [
    url(r'^password-required$', PasswordView.as_view(), name='password-required'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^$', FeedView.as_view(), name='feed'),
]
