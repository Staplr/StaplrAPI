from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FlashCardSerializer
from .models import FlashCard


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
        queryset = User.objects.all()
        serializer = UserSerializer