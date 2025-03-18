# models.py
from typing import Iterable
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.contrib import auth
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
from django.db.models.signals import post_save
from .utils import resize_image
from django.core.exceptions import ValidationError
from django.utils.timezone import now


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        # GlobalUserModel = apps.get_model(
        #     self.model._meta.app_label, self.model._meta.object_name
        # )
        # username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    # def with_perm(
    #     self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    # ):
    #     if backend is None:
    #         backends = auth._get_backends(return_tuples=True)
    #         if len(backends) == 1:
    #             backend, _ = backends[0]
    #         else:
    #             raise ValueError(
    #                 "You have multiple authentication backends configured and "
    #                 "therefore must provide the `backend` argument."
    #             )
    #     elif not isinstance(backend, str):
    #         raise TypeError(
    #             "backend must be a dotted import path string (got %r)." % backend
    #         )
    #     else:
    #         backend = auth.load_backend(backend)
    #     if hasattr(backend, "with_perm"):
    #         return backend.with_perm(
    #             perm,
    #             is_active=is_active,
    #             include_superusers=include_superusers,
    #             obj=obj,
    #         )
    #     return self.none()


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), blank=False)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_verified = models.BooleanField(
        _("verified"),
        default=False,
        help_text=_("Shows if this user varified their email. "),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    profile_picture = models.ImageField(
        upload_to="filmliste/profile_pictures/",
        blank=True,
        null=True,
        help_text=_("Upload a profile picture."),
    )

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"  # this makes their username their primary identifier
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_picture:
            resize_image(self.profile_picture.path)


@receiver(post_save, sender=CustomUser)
def resize_profile_picture(sender, instance, **kwargs):
    """sSignal to resize the profile picture after the user object is saved."""
    if instance.profile_picture:
        resize_image(instance.profile_picture.path)


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WatchProvider(models.Model):
    provider_id = models.AutoField(primary_key=True)
    provider_name = models.CharField(max_length=100)
    logo_path = models.CharField(max_length=255, null=True, blank=True)
    display_priority = models.IntegerField(default=0)

    def __str__(self):
        return self.provider_name


class Collection(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    overview = models.TextField(null=True, blank=True)
    poster_path = models.CharField(max_length=255, null=True, blank=True)
    backdrop_path = models.CharField(max_length=255, null=True, blank=True)

    def get_movies(self):
        return Movie.objects.filter(belongs_to_collection=self)

    def __str__(self):
        return self.name


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    backdrop_path = models.CharField(max_length=255, null=True, blank=True)
    belongs_to_collection = models.ForeignKey(
        Collection, on_delete=models.SET_NULL, null=True, blank=True
    )
    title = models.CharField(max_length=255)
    overview = models.TextField()
    release_date = models.DateField()
    runtime = models.IntegerField()
    popularity = models.FloatField()
    poster_path = models.CharField(max_length=255, null=True, blank=True)
    tagline = models.CharField(max_length=255, null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    providers_flatrate = models.ManyToManyField(
        WatchProvider, related_name="movie_providers_flatrate", blank=True
    )
    providers_rent = models.ManyToManyField(
        WatchProvider, related_name="movie_providers_rent", blank=True
    )
    providers_buy = models.ManyToManyField(
        WatchProvider, related_name="movie_providers_buy", blank=True
    )

    def __str__(self):
        return self.title


class TVSeries(models.Model):
    id = models.AutoField(primary_key=True)
    backdrop_path = models.CharField(max_length=255, null=True, blank=True)
    first_air_date = models.DateField()
    genres = models.ManyToManyField(Genre)
    last_air_date = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=255)
    number_of_seasons = models.IntegerField(default=0)
    number_of_episodes = models.IntegerField(default=0)
    overview = models.TextField()
    popularity = models.FloatField()
    poster_path = models.CharField(max_length=255, null=True, blank=True)
    tagline = models.CharField(max_length=255, null=True, blank=True)
    providers_flatrate = models.ManyToManyField(
        WatchProvider, related_name="tv_series_providers_flatrate", blank=True
    )
    providers_rent = models.ManyToManyField(
        WatchProvider, related_name="tv_series_providers_rent", blank=True
    )
    providers_buy = models.ManyToManyField(
        WatchProvider, related_name="tv_series_providers_buy", blank=True
    )

    def __str__(self):
        return self.name


class TVSeason(models.Model):
    id = models.AutoField(primary_key=True)
    air_date = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=255)
    overview = models.TextField()
    poster_path = models.CharField(max_length=255, null=True, blank=True)
    season_number = models.IntegerField()
    tv_series = models.ForeignKey(
        TVSeries, related_name="seasons", on_delete=models.CASCADE
    )
    # providers_flatrate = models.ManyToManyField(
    #     WatchProvider, related_name="tv_season_providers_flatrate", blank=True
    # )
    # providers_rent = models.ManyToManyField(
    #     WatchProvider, related_name="tv_season_providers_rent", blank=True
    # )
    # providers_buy = models.ManyToManyField(
    #     WatchProvider, related_name="tv_season_providers_buy", blank=True
    # )
    def __str__(self):
        return f"{self.tv_series.name} - Season {self.season_number}"


class TVEpisode(models.Model):
    id = models.AutoField(primary_key=True)
    episode_number = models.IntegerField()
    name = models.CharField(max_length=255)
    overview = models.TextField()
    runtime = models.IntegerField(null=True, blank=True)
    season_number = models.IntegerField()
    still_path = models.CharField(max_length=255, null=True, blank=True)
    season = models.ForeignKey(
        TVSeason, related_name="episodes", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.season.tv_series.name} - S{self.season_number}E{self.episode_number} - {self.name}"


class List(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="own_lists",
        null=False,
        blank=False,
    )
    users = models.ManyToManyField(CustomUser, related_name="shared_lists", blank=True)
    movies = models.ManyToManyField(Movie, blank=True)
    tv_series = models.ManyToManyField(TVSeries, blank=True)

    # Save titlecard colors + position to recreate radial gradient combo
    colors = models.JSONField(default=list, blank=True)

    def clean_colors(self):
        if not isinstance(self.colors, list) or len(self.colors) < 2:
            raise ValidationError(
                "The Color field must contain at least two dictionaries."
            )

        for entry in self.colors:
            if not isinstance(entry, dict):
                raise ValidationError("Each item in Color must be a dictionary.")

            for key, value in entry.items():
                if not isinstance(value, (int, float)):
                    raise ValidationError(
                        f"Value for '{key}' must be an integer or float."
                    )

    def save(self, **kwargs):
        self.clean_colors()
        return super().save(**kwargs)


class WatchAction(models.TextChoices):
    WATCHED = "watched", "Watched"  # has fully watched the movie/episode
    STARTED = "started", "Started"  # has started watching the tile/episod


class UserWatchHistory(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="watch_history"
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="watch_history",
    )
    episode = models.ForeignKey(
        TVEpisode,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="watch_history",
    )
    time = models.DateTimeField(default=now)
    action = models.CharField(
        max_length=10, choices=WatchAction.choices, default=WatchAction.WATCHED
    )

    class Meta:
        ordering = ["-time"]  # Show most recent watches first

    def __str__(self):
        if self.movie:
            return f"{self.user.username} watched {self.movie.title}"
        elif self.episode:
            return f"{self.user.username} watched {self.episode.season.tv_series.name} S{self.episode.season_number}E{self.episode.episode_number}"
        return f"{self.user.username} watch entry"
