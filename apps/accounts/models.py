from django.db import models
from pygments.lexers import get_all_lexers
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from pygments.styles import get_all_styles
from uuid import uuid4

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

    def to_json(self):
        student_arr = [student.id for student in self.students.all()]
        return {
            'Instructor': self.instructor.id,
            'Students': student_arr,
            'Name': self.name,
            'Description': self.description,
            'Class Identifier': self.class_identifier
        }


class Chapter(models.Model):
    course = models.ForeignKey(Course, related_name="chapters")
    description = models.TextField(max_length=200)
    order = models.IntegerField(default=None, null=True)


class Stapl(models.Model):
    chapter = models.ForeignKey(Chapter, related_name="stapls")
    date_created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="stapls")


class Poll(Stapl):
    active = models.BooleanField(default=True)


class Note(Stapl):
    text = models.TextField(max_length=10000)


class Deck(Stapl):
    name = models.CharField(max_length=20)


class FlashCard(models.Model):
    front = models.TextField(max_length=100)
    back = models.TextField(max_length=100)
    user = models.ForeignKey(User)
    deck = models.ForeignKey(Deck)


class Option(models.Model):
    text = models.TextField(max_length=200)
    poll = models.ForeignKey(Poll, related_name="options")


class Response(models.Model):
    option = models.ForeignKey(Option, related_name="responses")
    user = models.ForeignKey(User)
    poll = models.ForeignKey(Poll, related_name="responses")


class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comments")
    stapl = models.ForeignKey(Stapl, related_name="comments")
    date_created = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=1000)

