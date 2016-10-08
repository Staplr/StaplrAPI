from django.db import models
from pygments.lexers import get_all_lexers
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from pygments.styles import get_all_styles
from uuid import uuid4
import pyqrcode
import os
from django.conf import settings

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class UserManager(BaseUserManager):

    def create_user(self, username, email, password, name, **kwargs):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            name=name,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            is_staff=True,
            is_superuser=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'username'
    username = models.CharField(max_length=15, unique=True)
    objects = UserManager()
    email = models.EmailField(unique=True)
    name = models.TextField(max_length=40)

    def get_short_name(self):
        return self.username

    def to_json(self):
        takes = [course.id for course in self.courses.all()]
        teacher = [teach.id for teach in self.teaches.all()]
        return {
            'username': self.username,
            'email': self.email,
            'id': self.id,
            'teaches': teacher,
            'courses': takes,
        }


class Course(models.Model):
    instructor = models.ForeignKey(User, related_name="teaches")
    students = models.ManyToManyField(User, related_name="courses", null=True)
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200, blank=True)
    class_identifier = models.CharField(max_length=7, unique=True, default=str(uuid4())[:7])
    qrcode = models.FilePathField(blank=True)

    def to_json(self):
        student_arr = [student.id for student in self.students.all()]
        chapters = [chapter.id for chapter in self.chapters.all()]
        return {
            'Instructor': self.instructor.id,
            'Students': student_arr,
            'Name': self.name,
            'Description': self.description,
            'Chapters': chapters,
            'Class Identifier': self.class_identifier,
            'id': self.id,
            'qrcode': self.qrcode
        }

    def save(self, *args, **kwargs):
        if not self.qrcode:
            self.qrcode = settings.SITE_URL + '/media/' + self.class_identifier + ".png"
            if not os.path.exists(os.path.dirname(settings.MEDIA_ROOT + "/")):
                os.makedirs(os.path.dirname(settings.MEDIA_ROOT + "/"))
            pq = pyqrcode.create(self.class_identifier)
            pq.png(settings.MEDIA_ROOT + "/" + self.class_identifier + ".png", scale=6)
        super(Course, self).save(*args, **kwargs)


class Chapter(models.Model):
    course = models.ForeignKey(Course, related_name="chapters")
    description = models.TextField(max_length=200)
    order = models.IntegerField(default=None, null=True)
    name = models.CharField(max_length=20)

    def to_json(self):
        stapls = [stapl for stapl in self.stapls.all()]
        return {
            'Name': self.name,
            'Description': self.description,
            'course_id': self.course.id,
            'id': self.id,
            'order': self.order,
            'stapls': stapls,
        }


class Stapl(models.Model):
    chapter = models.ForeignKey(Chapter, related_name="stapls")
    date_created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="stapls")

    def to_json(self):
        return {
            'Chapter_id': self.chapter.id,
            'date_created': self.date_created,
            'user_id': self.user.id,
            'stapl_id': self.id,
        }


class Poll(Stapl):
    active = models.BooleanField(default=True)

    def to_json(self):
        responses = [response.id for response in self.responses.all()]
        options = [[option.id, option.text] for option in self.options.all()]
        comments = [comment.id for comment in self.comments.all()]
        return {
            'Chapter_id': self.chapter.id,
            'date_created': self.date_created,
            'user_id': self.user.id,
            'Responses': responses,
            'options': options,
            'stapl_id': self.id,
            'comments': comments
        }

    def get_percents(self):
        total = sum(option.responses.count() for option in self.options.all())
        if total > 0:
            percents = [[option.id, option.text, float(option.responses.count() / total) * 100] for option in self.options.all()]
        else:
            percents = "No responses"
        return {
            'results': percents
        }


class Note(Stapl):
    filepath = models.FilePathField()

    def to_json(self):
        comments = [comment.id for comment in self.comments.all()]
        return {
            'Chapter_id': self.chapter.id,
            'date_created': self.date_created,
            'user_id': self.user.id,
            'comments': comments,
            'filepath': self.filepath,
            'stapl_id': self.id

        }


class Deck(Stapl):
    name = models.CharField(max_length=20)

    def to_json(self):
        flashcards = [flashcard.id for flashcard in self.flashcards.all()]
        comments = [comment.id for comment in self.comments.all()]
        return {
            'Chapter_id': self.chapter.id,
            'date_created': self.date_created,
            'user_id': self.user.id,
            'comments': comments,
            'flashcards': flashcards,
            'stapl_id': self.id
        }


class FlashCard(models.Model):
    front = models.TextField(max_length=100)
    back = models.TextField(max_length=100)
    user = models.ForeignKey(User)
    deck = models.ForeignKey(Deck, related_name="flashcards")

    def to_json(self):
        return {
            'id': self.id,
            'front': self.front,
            'back': self.back,
            'user_id': self.user.id,
        }


class Option(models.Model):
    text = models.TextField(max_length=200)
    poll = models.ForeignKey(Poll, related_name="options")

    def to_json(self):
        responses = [response.id for response in self.responses.all()]
        return {
            "text": self.text,
            "poll_id": self.poll.id,
            "id": self.id,
            "responses": responses
        }


class Answer(models.Model):
    option = models.ForeignKey(Option, related_name="responses")
    user = models.ForeignKey(User)
    poll = models.ForeignKey(Poll, related_name="responses")

    def to_json(self):
        return {
            "poll_id": self.poll.id,
            "user_id": self.user.id,
            "option_id": self.option_id
        }


class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comments")
    stapl = models.ForeignKey(Stapl, related_name="comments")
    date_created = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=1000)

    def to_json(self):
        return {
            "stapl_id": self.stapl.id,
            "user_id": self.user.id,
            "text": self.text,
            "date_created": self.date_created
        }
