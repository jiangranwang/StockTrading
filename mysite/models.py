# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from math import ceil

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

from comment.managers import CommentManager
from comment.conf import settings
from comment.utils import is_comment_moderator


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()
    urlhash = models.CharField(
        max_length=50,
        unique=True,
        editable=False
        )
    posted = models.DateTimeField(default=timezone.now, editable=False)
    edited = models.DateTimeField(auto_now=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-posted', ]

    def __str__(self):
        username = self.get_username()
        _content = self.content[:20]
        if not self.parent:
            return f'comment by {username}: {_content}'
        else:
            return f'reply by {username}: {_content}'

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            'user': self.user,
            'content': self.content,
            'email': self.email,
            'posted': str(self.posted),
            'app_name': self.content_type.app_label,
            'model_name': self.content_type.model,
            'model_id': self.object_id,
            'parent': getattr(self.parent, 'id', None)
        }

    def _get_reaction_count(self, reaction_type):
        return getattr(self.reaction, reaction_type, None)

    def replies(self, include_flagged=False):
        manager = self.__class__.objects
        if include_flagged:
            qs = manager.all()
        else:
            qs = manager.all_exclude_flagged()

        return manager._filter_parents(qs, parent=self)

    def _set_unique_urlhash(self):
        if not self.urlhash:
            self.urlhash = self.__class__.objects.generate_urlhash()
            while self.__class__.objects.filter(urlhash=self.urlhash).exists():
                self.urlhash = self.__class__.objects.generate_urlhash()

    def _set_email(self):
        if self.user:
            self.email = getattr(self.user, self.user.EMAIL_FIELD, '')

    def _get_username_for_anonymous(self):
        if settings.COMMENT_USE_EMAIL_FIRST_PART_AS_USERNAME:
            return self.email.split('@')[0]

        return settings.COMMENT_ANONYMOUS_USERNAME

    def get_username(self):
        user = self.user
        if not user:
            return self._get_username_for_anonymous()

        return getattr(user, user.USERNAME_FIELD)

    def save(self, *args, **kwargs):
        self._set_unique_urlhash()
        self._set_email()
        super(Comment, self).save(*args, **kwargs)

    def get_url(self, request):
        page_url = self.content_object.get_absolute_url()
        comments_per_page = settings.COMMENT_PER_PAGE
        if comments_per_page:
            qs_all_parents = self.__class__.objects.filter_parents_by_object(
                self.content_object, include_flagged=is_comment_moderator(request.user)
                )
            position = qs_all_parents.filter(posted__gte=self.posted).count() + 1
            if position > comments_per_page:
                page_url += '?page=' + str(ceil(position / comments_per_page))
        return page_url + '#' + self.urlhash

    @property
    def is_parent(self):
        return self.parent is None

    @property
    def is_edited(self):
        if self.user:
            return self.posted.timestamp() + 1 < self.edited.timestamp()
        return False

    @property
    def likes(self):
        return self._get_reaction_count('likes')

    @property
    def dislikes(self):
        return self._get_reaction_count('dislikes')

    @property
    def is_flagged(self):
        if hasattr(self, 'flag') and self.flag.is_flag_enabled:
            return self.flag.state != self.flag.UNFLAGGED
        return False

    @property
    def has_flagged_state(self):
        if hasattr(self, 'flag'):
            return self.flag.state == self.flag.FLAGGED
        return False

    @property
    def has_rejected_state(self):
        if hasattr(self, 'flag'):
            return self.flag.state == self.flag.REJECTED
        return False

    @property
    def has_resolved_state(self):
        if hasattr(self, 'flag'):
            return self.flag.state == self.flag.RESOLVED
        return False


class Chat(models.Model):
    chatid = models.IntegerField(db_column='ChatId', primary_key=True)  # Field name made lowercase.
    senderid = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='SenderId', blank=True, null=True)  # Field name made lowercase.
    receiver = models.ForeignKey('Room', models.DO_NOTHING, db_column='Receiver', blank=True, null=True)  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Chat'


class Market(models.Model):
    marketid = models.IntegerField(db_column='MarketId', primary_key=True)  # Field name made lowercase.
    marketname = models.CharField(db_column='MarketName', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Market'


class Room(models.Model):
    roomid = models.IntegerField(db_column='RoomId', primary_key=True)  # Field name made lowercase.
    groupname = models.CharField(db_column='GroupName', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Room'


class Roomrelation(models.Model):
    roomid = models.OneToOneField(Room, models.DO_NOTHING, db_column='RoomId', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='UserId')  # Field name made lowercase.
    ismanager = models.IntegerField(db_column='isManager', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RoomRelation'
        unique_together = (('roomid', 'userid'),)


class Stock(models.Model):
    stockid = models.IntegerField(db_column='StockId', primary_key=True)  # Field name made lowercase.
    marketid = models.ForeignKey(Market, models.DO_NOTHING, db_column='MarketID')  # Field name made lowercase.
    stockname = models.CharField(db_column='StockName', max_length=255)  # Field name made lowercase.
    price = models.FloatField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    high = models.FloatField(db_column='High', blank=True, null=True)  # Field name made lowercase.
    low = models.FloatField(db_column='Low', blank=True, null=True)  # Field name made lowercase.
    volume = models.FloatField(db_column='Volume', blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='Company', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Stock'


class Stockprice(models.Model):
    priceid = models.AutoField(db_column='PriceId', primary_key=True)  # Field name made lowercase.
    stockid = models.ForeignKey(Stock, models.DO_NOTHING, db_column='StockId', blank=True, null=True)  # Field name made lowercase.
    price = models.FloatField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'StockPrice'

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    #id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'



class Watchlist(models.Model):
    UserId = models.OneToOneField(AuthUser, models.DO_NOTHING, db_column='id', primary_key=True)  # Field name made lowercase.
    StockId = models.ForeignKey(Stock, models.DO_NOTHING, db_column='StockId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Watchlist'
        unique_together = (('UserId', 'StockId'),)




class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
