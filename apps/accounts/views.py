from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FlashCardSerializer, UserSerializer
from .models import FlashCard, User, Course
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
    if 'id' in request.data and User.objects.filter(id=request.data['id']).exists():
        course = Course.objects.get(id=request.data['id'])
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


class CourseView(APIView):

    permission_classes = ()

    def post(self, request, format=None):
        if all(name in request.data for name in ['instructor_id', 'description', 'name']):
            course = Course()
            if not User.objects.filter(id=request.data['instructor_id']).exists():
                return Response({'Invalid Instructor Id'}, status=status.HTTP_404_NOT_FOUND)
            course.instructor = User.objects.get(id=request.data['instructor_id'])
            course.description = request.data['description']
            course.name = request.data['name']
            course.save()
            return Response({"Good job mate!"}, status=status.HTTP_201_CREATED)
        return Response({'Not all data present. (Instructor, description, name)'}, status=status.HTTP_404_NOT_FOUND)
