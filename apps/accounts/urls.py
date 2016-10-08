from django.conf.urls import url, include
from rest_framework import routers
from .views import FlashCardView, UserView, get_user_for_id, CourseView, add_to_course

router = routers.DefaultRouter()


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^users/$', UserView.as_view()),
    url(r'^course/$', CourseView.as_view()),
    url(r'^add_to_course/$', add_to_course),
    url(r'^user/$', get_user_for_id),
    url(r'^flashcards/$', FlashCardView.as_view()),
    url(r'^', include(router.urls)),
]