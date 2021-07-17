from .views import EventViewSet, SummaryViewSet, DateViewSet, UserRegistrationView, UserLoginView, UserProfileView
from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers


router = routers.DefaultRouter()
router.register('events', EventViewSet)
router.register('summarys', SummaryViewSet)
router.register('dates', DateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    url(r'^signup', UserRegistrationView.as_view(), name='signup'),
    url(r'^signin', UserLoginView.as_view(), name='signin'),
    url(r'^profile', UserProfileView.as_view()),
]
