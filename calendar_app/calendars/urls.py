from . import views
from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers


router = routers.DefaultRouter()
router.register('calendars', views.CalendarView)
router.register('events', views.ItemView)

urlpatterns = [
    # path('/', include('calendars.url')),
    path('', include(router.urls)),
    url(r'^signup', views.UserRegistrationView.as_view(), name='signup'),
    url(r'^signin', views.UserLoginView.as_view(), name='signin'),
    url(r'^profile', views.UserProfileView.as_view()),
]
