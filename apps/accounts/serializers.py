from rest_framework import serializers
from .models import FlashCard, User, Comment, Deck, Option, Response, Note, Poll, Chapter, Course


class UserSerializer(serializers.HyperlinkedModelSerializer):
    courses = serializers.PrimaryKeyRelatedField(many=True)
    teaches = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'courses', 'teaches')


class FlashCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlashCard
        fields = ('id', 'front', 'back')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id')


class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.PrimaryKeyRelatedField(read_only=True)
