from django.conf.urls import url, include
from rest_framework import routers
from .views import FlashCardView

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^flashcards/$', FlashCardView.as_view()),
    url(r'^', include(router.urls)),
]