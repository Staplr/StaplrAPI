from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import FlashCard, User, Course, Chapter, Stapl, Poll, Option, Deck, Note, Answer, Comment
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate

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
                return Response({'Error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)
            User.objects.get(id=request.data["id"]).delete()
            return Response({'Message': 'User Deleted'}, status=status.HTTP_200_OK)
        return Response({'Id not found'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes('')
def get_user_for_id(request):
    if 'id' in request.data and User.objects.filter(id=request.data['id']).exists():
        user = User.objects.get(id=request.data['id'])
        return Response(user.to_json(), status=status.HTTP_200_OK)
    return Response({'Id not found'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes('')
def login_user(request):
    if all(name in request.data for name in ['username', 'password']):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({"User": user.to_json()})
        return Response({"Error": "Invalid password or username."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"Error": 'Invalid Credentals (username, password)'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes('')
def course_from_id(request):
    if 'course_id' in request.data and Course.objects.filter(id=request.data['course_id']).exists():
        course = Course.objects.get(id=request.data['course_id'])
        return Response(course.to_json(), status=status.HTTP_200_OK)
    return Response({'Id not found'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes('')
def add_to_course(request):
    if 'course_id' in request.data and 'student_id' in request.data:
            if not User.objects.filter(id=request.data['student_id']).exists():
                return Response({'Invalid student_id'}, status=status.HTTP_400_BAD_REQUEST)
            if not Course.objects.filter(id=request.data['course_id']):
                return Response({'Invalid course_id'}, status=status.HTTP_400_BAD_REQUEST)
            course = Course.objects.get(id=request.data['course_id'])
            course.students.add(request.data['student_id'])
            return Response(course.to_json(), status=status.HTTP_200_OK)
    return Response({'Not all data present. (course_id, student_id)'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes('')
def remove_from_course(request):
    if 'course_id' in request.data and 'student_id' in request.data:
            if not User.objects.filter(id=request.data['student_id']).exists():
                return Response({'Invalid student_id'}, status=status.HTTP_400_BAD_REQUEST)
            if not Course.objects.filter(id=request.data['course_id']):
                return Response({'Invalid course_id'}, status=status.HTTP_400_BAD_REQUEST)
            course = Course.objects.get(id=request.data['course_id'])
            if course.students.filter(id=request.data['student_id']):
                course.students.get(id=request.data['student_id']).delete()
            return Response(course.to_json(), status=status.HTTP_200_OK)
    return Response({'Not all data present. (course_id, student_id)'}, status=status.HTTP_400_BAD_REQUEST)


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
                return Response({'Invalid Instructor Id'}, status=status.HTTP_400_BAD_REQUEST)
            course.instructor = User.objects.get(id=request.data['instructor_id'])
            course.description = request.data['description']
            course.name = request.data['name']
            course.save()
            return Response(course.to_json(), status=status.HTTP_201_CREATED)
        return Response({'Not all data present. (Instructor, description, name)'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        if "course_id" in request.data:
            try:
                course = Course.objects.get(id=request.data["course_id"])
            except Course.DoesNotExist:
                course = None
            if course is None:
                return Response({'Error': 'Course not found.'}, status=status.HTTP_400_BAD_REQUEST)
            course.delete()
            return Response({'Message': 'Course Deleted'}, status=status.HTTP_200_OK)
        return Response({'Id not found'}, status=status.HTTP_400_BAD_REQUEST)


class ChapterView(APIView):

    permission_classes = ()

    def post(self, request, format=None):
        if all(name in request.data for name in ['course_id', 'description', 'name']):
            chapter = Chapter()
            if not Course.objects.filter(id=request.data['course_id']).exists():
                return Response({'Error': 'Course not found.'}, status=status.HTTP_400_BAD_REQUEST)
            course = Course.objects.get(id=request.data['course_id'])
            count = course.chapters.count()
            chapter.order = count + 1
            chapter.course = course
            chapter.description = request.data['description']
            chapter.name = request.data['name']
            chapter.save()
            return Response(chapter.to_json(), status=status.HTTP_201_CREATED)
        return Response({'Not all data present. (course_id, description, name)'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        if "chapter_id" in request.data:
            try:
                chapter = Chapter.objects.get(id=request.data["chapter_id"])
            except Chapter.DoesNotExist:
                chapter = None
            if chapter is None:
                return Response({'Error': 'Chapter not found.'}, status=status.HTTP_400_BAD_REQUEST)
            chapter.delete()
            return Response({'Message': 'Chapter Deleted'}, status=status.HTTP_200_OK)
        return Response({'Id not found'}, status=status.HTTP_400_BAD_REQUEST)

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
    return Response({"Error": 'Id not found'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes('')
def chapter_from_course(request):
    if 'course_id' in request.data and Course.objects.filter(id=request.data['course_id']).exists():
        course = Course.objects.get(id=request.data['course_id'])
        chapters = [chapter.to_json() for chapter in course.chapters.all()]
        return Response({"Chapters": chapters}, status=status.HTTP_200_OK)
    return Response({"Error": 'Id not found'}, status=status.HTTP_400_BAD_REQUEST)


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
                return Response({'Error': 'Stapl not found.'}, status=status.HTTP_400_BAD_REQUEST)
            stapl.delete()
            return Response({'Message': 'Stapl Deleted'}, status=status.HTTP_200_OK)
        return Response({'Id not found'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes('')
def poll_from_chapter(request):
    if all(name in request.data for name in ['chapter_id', 'options', 'user_id']):
        if not Chapter.objects.filter(id=request.data['chapter_id']).exists():
            return Response({'Invalid chapter Id'}, status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(id=request.data['user_id']).exists():
            return Response({'Invalid user Id'}, status=status.HTTP_400_BAD_REQUEST)
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
    return Response({"Error": 'Invalid parameters. (chapter_id, options[], user_id)'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes('')
def set_poll_inactive(request):
    if 'stapl_id' in request.data:
        if not Stapl.objects.filter(id=request.data['stapl_id']):
            return Response({'Invalid poll Id'}, status=status.HTTP_400_BAD_REQUEST)
        poll = Poll.objects.get(id=request.data['stapl_id'])
        poll.active = False
        poll.save()
        return Response({"Message": "Successfully set poll to inactive"}, status=status.HTTP_200_OK)
    return Response({"Error": "Invalid parameters (stapl_id)"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes('')
def poll_results(request):
    if 'stapl_id' in request.data:
        if not Stapl.objects.filter(id=request.data['stapl_id']):
            return Response({'Invalid poll Id'}, status=status.HTTP_400_BAD_REQUEST)
        poll = Poll.objects.get(id=request.data['stapl_id'])
        return Response(poll.get_percents(), status=status.HTTP_200_OK)
    return Response({"Error": "Invalid parameters (stapl_id)"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes('')
def answer_poll(request):
    if all(name in request.data for name in ['stapl_id', 'user_id', 'option_id']):
        if not Option.objects.filter(id=request.data['option_id']):
            return Response({'Invalid option Id'}, status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(id=request.data['user_id']).exists():
            return Response({'Invalid user Id'}, status=status.HTTP_400_BAD_REQUEST)
        if not Stapl.objects.filter(id=request.data['stapl_id']).exists():
            return Response({'Invalid stapl Id'}, status=status.HTTP_400_BAD_REQUEST)
        option = Option.objects.get(id=request.data['option_id'])
        answer = Answer()
        answer.option = option
        user = User.objects.get(id=request.data['user_id'])
        answer.user = user
        answer.poll = Poll.objects.get(id=request.data['stapl_id'])
        answer.save()
        return Response(answer.to_json(), status=status.HTTP_200_OK)
    return Response({"Error": "Invalid parameters (stapl_id, user_id, option_id)"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes('')
def note_from_chapter(request):
    if all(name in request.data for name in ['chapter_id', 'user_id', 'text']):
        if not Chapter.objects.filter(id=request.data['chapter_id']).exists():
            return Response({'Invalid chapter Id'}, status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(id=request.data['user_id']).exists():
            return Response({'Invalid user Id'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=request.data['user_id'])
        chapter = Chapter.objects.get(id=request.data['chapter_id'])
        note = Note()
        note.chapter = chapter
        note.user = user
        note.text = request.data['text']
        note.save()
        return Response(note.to_json(), status=status.HTTP_200_OK)
    return Response({"Error": 'Invalid parameters. (chapter_id, options[], user_id)'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes('')
def deck_from_chapter(request):
    if all(name in request.data for name in ['chapter_id', 'user_id']):
        if not Chapter.objects.filter(id=request.data['chapter_id']).exists():
            return Response({'Invalid chapter Id'}, status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(id=request.data['user_id']).exists():
            return Response({'Invalid user Id'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=request.data['user_id'])
        chapter = Chapter.objects.get(id=request.data['chapter_id'])
        deck = Deck()
        deck.chapter = chapter
        deck.user = user
        deck.save()
        return Response(deck.to_json(), status=status.HTTP_200_OK)
    return Response({"Error": 'Invalid parameters. (chapter_id, user_id)'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes('')
def flashcard_from_deck(request):
    if all(name in request.data for name in ['front', 'back', 'deck_id', 'user_id']):
        if not Deck.objects.filter(id=request.data['deck_id']).exists():
            return Response({'Invalid deck Id'}, status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(id=request.data['user_id']).exists():
            return Response({'Invalid user Id'}, status=status.HTTP_400_BAD_REQUEST)
        flash = FlashCard()
        flash.front = request.data['front']
        flash.back = request.data['back']
        flash.user = User.objects.get(id=request.data['user_id'])
        flash.deck = Deck.objects.get(id=request.data['deck_id'])
        flash.save()
        return Response(flash.to_json(), status=status.HTTP_200_OK)
    return Response({"Error": 'Invalid parameters. (front,back, deck_id, user_id)'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes('')
def remove_flashcard(request):
    if 'flashcard_id' in request.data and FlashCard.objects.filter(id=request.data['flashcard_id']).exists():
        FlashCard.objects.get(id=request.data['flashcard_id'])
        return Response({'Message': 'FlashCard was removed'}, status=status.HTTP_200_OK)
    return Response({"Error": 'Invalid flashcard_id'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes('')
def comments_for_stapl(request):
    if 'stapl_id' in request.data:
        if not Stapl.objects.filter(id=request.data['stapl_id']).exists():
            return Response({'Invalid stapl Id'}, status=status.HTTP_400_BAD_REQUEST)
        stapl = Stapl.objects.get(id=request.data['stapl_id'])
        comments = [comment.to_json() for comment in stapl.comments.all().order_by('-date_created')]
        return Response({"Comments": comments}, status=status.HTTP_200_OK)
    return Response({"Error": 'Invalid parameters. (stapl_id)'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes('')
def create_comment(request):
    if all(name in request.data for name in ['stapl_id', 'user_id', 'comment']):
        if not Stapl.objects.filter(id=request.data['stapl_id']).exists():
            return Response({'Invalid deck Id'}, status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(id=request.data['user_id']).exists():
            return Response({'Invalid user Id'}, status=status.HTTP_400_BAD_REQUEST)
        comment = Comment()
        comment.user = User.objects.get(id=request.data['user_id'])
        comment.stapl = Stapl.objects.get(id=request.data['stapl_id'])
        comment.text = request.data['comment']
        comment.save()
        return Response(comment.to_json(), status=status.HTTP_201_CREATED)
    return Response({"Error": 'Invalid parameters. (stapl_id, user_id, text)'}, status=status.HTTP_400_BAD_REQUEST)



class FileUploadView(APIView):
    parser_classes = (FileUploadParser, )
    permission_classes = ()

    def post(self, request, format='jpg'):
        up_file = request.FILES['file']
        destination = open('/Users/Username/' + up_file.name, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
            destination.close()