from django.conf.urls import url, include
from rest_framework import routers
from .views import (
    UserView, get_user_for_id, CourseView, add_to_course,
    course_from_id, remove_from_course, ChapterView, chapter_from_id, chapter_from_course,
    StaplsView, poll_from_chapter, poll_results, answer_poll, note_from_chapter, deck_from_chapter,
    flashcard_from_deck, comments_for_stapl, create_comment
)

router = routers.DefaultRouter()


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^users/$', UserView.as_view()),
    url(r'^stapls/$', StaplsView.as_view()),
    url(r'^course/$', CourseView.as_view()),
    url(r'^chapter/$', ChapterView.as_view()),
    url(r'^get_course/$', course_from_id),
    url(r'^add_to_course/$', add_to_course),
    url(r'^remove_from_course/$', remove_from_course),
    url(r'^course_from_id/$', course_from_id),
    url(r'^poll_from_chapter/$', poll_from_chapter),
    url(r'^chapter_from_id/$', chapter_from_id),
    url(r'^chapter_from_course/$', chapter_from_course),
    url(r'^poll_results/$', poll_results),
    url(r'^answer_poll/$', answer_poll),
    url(r'^note_from_chapter/$', note_from_chapter),
    url(r'^flashcard_from_deck/$', flashcard_from_deck),
    url(r'^deck_from_chapter/$', deck_from_chapter),
    url(r'^comments_for_stapl/$', comments_for_stapl),
    url(r'^create_comment/$', create_comment),
    url(r'^user/$', get_user_for_id),
    url(r'^', include(router.urls)),
]