from rest_framework import serializers
from .models import FlashCard, User, Comment, Deck, Option, Answer, Note, Poll, Chapter, Course


class UserSerializer(serializers.HyperlinkedModelSerializer):
    courses = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    teaches = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

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
    students = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'instructor', 'students', 'description', 'class_identifier')


class PollSerializer(serializers.ModelSerializer):
    options = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ('id', 'options', 'active')

