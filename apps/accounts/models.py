from django.db import models
from pygments.lexers import get_all_lexers
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from pygments.styles import get_all_styles
from uuid import uuid4

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class UserManager(BaseUserManager):

    def create_user(self, username, email, password, **kwargs):
        user = self.model(
            username=username
            email=self.normalize_email(email),
            is_active=True,
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


class Course(models.Model):
    instructor = models.ForeignKey(User, related_name="teaches")
    students = models.ManyToMany(User, related_name="courses")
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)
    qrcode = models.CharField(max_length=7, unique=True, default=str(uuid4())[:7])


class Chapter(models.Model):
    course = models.ForeignKey(Course, related_name="chapters")
    description = models.TextField(max_length=200)
    order = models.IntegerField(null=True)


class Stapl(models.Model):
    chapter = models.ForeignKey(Chapter, related_name="stapls")
    date_created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="stapls")


class Poll(Stapl):
    active = models.BooleanField(default=True)


class Note(Stapl):
    text = models.TextField(max_length=10000)


class FlashCard(models.Model):
    front = models.TextField(max_length=100)
    back = models.TextField(max_length=100)
    user = models.ForeignKey(User)


class Option(models.Model):
    text = models.TextField(max_length=200)
    poll = models.ForeignKey(Poll, related_name="options")


class Response(models.Model):
    option = models.ForeignKey(option, related_name="responses")
    user = models.ForeignKey(User)
    poll = models.ForeignKey(Poll, related_name="responses")


class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comments")
    stapl = models.ForeignKey(stapl, related_name="comments")
    date_created = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=1000)


