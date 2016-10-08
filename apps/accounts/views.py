from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FlashCardSerializer, UserSerializer
from .models import FlashCard, User, Course, Chapter, Stapl, Poll, Option, Deck, Note, Answer
from rest_framework.decorators import api_view, permission_classes


class FlashCardView(APIView):
    """
    List out all flashcards
    """
    permission_classes = ()

    def get(self, request, format=None):
        queryset = FlashCard.objects.all().order_by('date_created')
        serializer = FlashCardSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FlashCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):
        if "id" in request.data:
            try:
                flashcard = FlashCard.objects.get(id=request.data["id"])
            except FlashCard.DoesNotExist:
                flashcard = None
            if flashcard is None:
                return Response({'Error': 'Flashcard not found.'}, status=status.HTTP_404_NOT_FOUND)
            FlashCard.objects.get(id=request.data["id"]).delete()
            return Response({'Message': 'Flashcard Deleted'}, status=status.HTTP_200_OK)


class UserView(APIView):

    permission_classes = ()

    def get(self, request, format=None):
        users = [user.to_json() for user in User.objects.all()]
        return Response({
            'Users': users
        }, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            try:
                user = User.objects.create_user(
                    request.data['username'],
                    request.data['email'],
                    request.data['password'],
                    request.data['name'],
                )
                return Response(user.to_json(), status=status.HTTP_201_CREATED)
            except Exception:
                return Response({"Invalid fields."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        if "id" in request.data:
            try:
                user = User.objects.get(id=request.data["id"])
            except User.DoesNotExist:
                user = None
            if user is None:
                return Response({'Error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
            User.objects.get(id=request.data["id"]).delete()
            return Response({'Message': 'User Deleted'}, status=status.HTTP_200_OK)
        return Response({'Id not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes('')
def get_user_for_id(request):
    if 'id' in request.data and User.objects.filter(id=request.data['id']).exists():
        user = User.objects.get(id=request.data['id'])
        return Response(user.to_json(), status=status.HTTP_200_OK)
    return Response({'Id not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes('')
def course_from_id(request):
    if 'course_id' in request.data and Course.objects.filter(id=request.data['course_id']).exists():
        course = Course.objects.get(id=request.data['course_id'])
        return Response(course.to_json(), status=status.HTTP_200_OK)
    return Response({'Id not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes('')
def add_to_course(request):
    if 'course_id' in request.data and 'student_id' in request.data:
            if not User.objects.filter(id=request.data['student_id']).exists():
                return Response({'Invalid student_id'}, status=status.HTTP_404_NOT_FOUND)
            if not Course.objects.filter(id=request.data['course_id']):
                return Response({'Invalid course_id'}, status=status.HTTP_404_NOT_FOUND)
            course = Course.objects.get(id=request.data['course_id'])
            course.students.add(request.data['student_id'])
            return Response(course.to_json(), status=status.HTTP_200_OK)
    return Response({'Not all data present. (course_id, student_id)'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes('')
def remove_from_course(request):
    if 'course_id' in request.data and 'student_id' in request.data:
            if not User.objects.filter(id=request.data['student_id']).exists():
                return Response({'Invalid student_id'}, status=status.HTTP_404_NOT_FOUND)
            if not Course.objects.filter(id=request.data['course_id']):
                return Response({'Invalid course_id'}, status=status.HTTP_404_NOT_FOUND)
            course = Course.objects.get(id=request.data['course_id'])
            if course.students.filter(id=request.data['student_id']):
                course.students.get(id=request.data['student_id']).delete()
            return Response(course.to_json(), status=status.HTTP_200_OK)
    return Response({'Not all data present. (course_id, student_id)'}, status=status.HTTP_404_NOT_FOUND)


class CourseView(APIView):

    permission_classes = ()

    def get(self, request, format=None):
        courses = [course.to_json() for course in Course.objects.all()]
        return Response({
            "Courses": courses
        }, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        if all(name in request.data for name in ['instructor_id', 'description', 'name']):
            course = Course()
            if not User.objects.filter(id=request.data['instructor_id']).exists():
                return Response({'Invalid Instructor Id'}, status=status.HTTP_404_NOT_FOUND)
            course.instructor = User.objects.get(id=request.data['instructor_id'])
            course.description = request.data['description']
            course.name = request.data['name']
            course.save()
            return Response(course.to_json(), status=status.HTTP_201_CREATED)
        return Response({'Not all data present. (Instructor, description, name)'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, format=None):
        if "course_id" in request.data:
            try:
                course = Course.objects.get(id=request.data["course_id"])
            except Course.DoesNotExist:
                course = None
            if course is None:
                return Response({'Error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
            course.delete()
            return Response({'Message': 'Course Deleted'}, status=status.HTTP_200_OK)
        return Response({'Id not found'}, status=status.HTTP_404_NOT_FOUND)


class ChapterView(APIView):

    permission_classes = ()

    def post(self, request, format=None):
        if all(name in request.data for name in ['course_id', 'description', 'name']):
            chapter = Chapter()
            if not Course.objects.filter(id=request.data['course_id']).exists():
                return Response({'Error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
            course = Course.objects.get(id=request.data['course_id'])
            count = course.chapters.count()
            chapter.order = count + 1
            chapter.course = course
            chapter.description = request.data['description']
            chapter.name = request.data['name']
            chapter.save()
            return Response(chapter.to_json(), status=status.HTTP_201_CREATED)
        return Response({'Not all data present. (course_id, description, name)'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, format=None):
        if "chapter_id" in request.data:
            try:
                chapter = Chapter.objects.get(id=request.data["chapter_id"])
            except Chapter.DoesNotExist:
                chapter = None
            if chapter is None:
                return Response({'Error': 'Chapter not found.'}, status=status.HTTP_404_NOT_FOUND)
            chapter.delete()
            return Response({'Message': 'Chapter Deleted'}, status=status.HTTP_200_OK)
        return Response({'Id not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, format=None):
        chapters = [chapter.get_json() for chapter in Chapter.objects.all()]
        return Response({
            'Chapters': chapters
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes('')
def chapter_from_id(request):
    if 'chapter_id' in request.data and Chapter.objects.filter(id=request.data['chapter_id']).exists():
        chapter = Chapter.objects.get(id=request.data['chapter_id'])
        return Response(chapter.to_json(), status=status.HTTP_200_OK)
    return Response({"Error": 'Id not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes('')
def chapter_from_course(request):
    if 'course_id' in request.data and Course.objects.filter(id=request.data['course_id']).exists():
        course = Course.objects.get(id=request.data['course_id'])
        chapters = [chapter.to_json() for chapter in course.chapters.all()]
        return Response({"Chapters": chapters}, status=status.HTTP_200_OK)
    return Response({"Error": 'Id not found'}, status=status.HTTP_404_NOT_FOUND)


class StaplsView(APIView):

    permission_classes = ()

    def get(self, request, format=None):
        stapls = [poll.to_json() for poll in Poll.objects.all()]
        stapls.extend([note.to_json() for note in Note.objects.all()])
        stapls.extend([deck.to_json() for deck in Deck.objects.all()])
        stapls.sort(key=lambda x: x['stapl_id'], reverse=False)
        return Response({"Stapls": stapls}, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        if "stapl_id" in request.data:
            try:
                stapl = Stapl.objects.get(id=request.data["stapl_id"])
            except Stapl.DoesNotExist:
                stapl = None
            if stapl is None:
                return Response({'Error': 'Stapl not found.'}, status=status.HTTP_404_NOT_FOUND)
            stapl.delete()
            return Response({'Message': 'Stapl Deleted'}, status=status.HTTP_200_OK)
        return Response({'Id not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes('')
def poll_from_chapter(request):
    if all(name in request.data for name in ['chapter_id', 'options', 'user_id']):
        if not Chapter.objects.filter(id=request.data['chapter_id']).exists():
            return Response({'Invalid chapter Id'}, status=status.HTTP_404_NOT_FOUND)
        if not User.objects.filter(id=request.data['user_id']).exists():
            return Response({'Invalid user Id'}, status=status.HTTP_404_NOT_FOUND)
        user = User.objects.get(id=request.data['user_id'])
        chapter = Chapter.objects.get(id=request.data['chapter_id'])
        poll = Poll()
        poll.chapter = chapter
        poll.user = user
        poll.save()
        for item in request.data.getlist('options'):
            option = Option()
            option.text = item
            option.poll = poll
            option.save()
        return Response(poll.to_json(), status=status.HTTP_200_OK)
    return Response({"Error": 'Invalid parameters. (chapter_id, options[], user_id)'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes('')
def set_poll_inactive(request):
    if 'stapl_id' in request.data:
        if not Stapl.objects.filter(id=request.data['stapl_id']):
            return Response({'Invalid poll Id'}, status=status.HTTP_404_NOT_FOUND)
        poll = Poll.objects.get(id=request.data['stapl_id'])
        poll.active = False
        poll.save()
        return Response({"Message": "Successfully set poll to inactive"}, status=status.HTTP_200_OK)
    return Response({"Error": "Invalid parameters (stapl_id)"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes('')
def poll_results(request):
    if 'stapl_id' in request.data:
        if not Stapl.objects.filter(id=request.data['stapl_id']):
            return Response({'Invalid poll Id'}, status=status.HTTP_404_NOT_FOUND)
        poll = Poll.objects.get(id=request.data['stapl_id'])
        return Response(poll.get_percents(), status=status.HTTP_200_OK)
    return Response({"Error": "Invalid parameters (stapl_id)"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes('')
def answer_poll(request):
    if all(name in request.data for name in ['stapl_id', 'user_id', 'option_id']):
        if not Option.objects.filter(id=request.data['option_id']):
            return Response({'Invalid option Id'}, status=status.HTTP_404_NOT_FOUND)
        if not User.objects.filter(id=request.data['user_id']).exists():
            return Response({'Invalid user Id'}, status=status.HTTP_404_NOT_FOUND)
        if not Stapl.objects.filter(id=request.data['stapl_id']).exists():
            return Response({'Invalid stapl Id'}, status=status.HTTP_404_NOT_FOUND)
        option = Option.objects.get(id=request.data['option_id'])
        answer = Answer()
        answer.option = option
        user = User.objects.get(id=request.data['user_id'])
        answer.user = user
        answer.poll = Poll.objects.get(id=request.data['stapl_id'])
        answer.save()
        return Response(answer.to_json(), status=status.HTTP_200_OK)
    return Response({"Error": "Invalid parameters (stapl_id, user_id, option_id)"}, status=status.HTTP_404_NOT_FOUND)
