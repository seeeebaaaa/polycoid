from requests.exceptions import HTTPError
from .models import Genre, Movie, Collection, WatchProvider
import tmdbsimple as tmdb
from rest_framework.response import Response
from datetime import datetime


def tmdb_catch(endpoint,**kwargs):
    """Returns None if 404 or any other error, else just reponse"""
    try:
        result = endpoint(**kwargs)
        return result
    except HTTPError as e:
        return None


def genres_get_or_create(genres_list: list[dict]):
    """Returns Queryset of Genres given. If not already existent, created DB entries for genres."""
    # create genres unless it exists already
    genres = []
    # check if all genres already exist in db
    if not Genre.objects.filter(id__in=[g["id"] for g in genres_list]).count() == len(
        genres_list
    ):
        # if not, create the missing ones
        for genre in genres_list:
            if not Genre.objects.filter(id=genre["id"]).exists():
                new_genre = Genre(id=genre["id"], name=genre["name"])
                new_genre.save()

    # get all gernes objects
    genres = Genre.objects.filter(id__in=[g["id"] for g in genres_list])
    return genres


def movie_get_or_create(movie_id: int,create_collection:bool=True):
    # try db first, then tmdb
    movie_qs = Movie.objects.filter(id=movie_id)
    if movie_qs.exists():
        movie = movie_qs[0]  # there can only be one, cause id is pk
    else:
        # query from tmdb instead and create db entry
        req_movie = tmdb.Movies(id=movie_id)
        details = tmdb_catch(req_movie.info)
        if not details:
            return Response({"error": "Invalid Movie ID"}, status=404)
        print(details)
        # create movie db record
        movie = Movie(
            id=details["id"],
            backdrop_path=details["backdrop_path"],
            title=details["title"],
            overview=details["overview"],
            release_date=datetime.strptime(
                details["release_date"], "%Y-%m-%d"
            ).date(),  # parse to date format
            runtime=details["runtime"],
            popularity=details["popularity"],
            poster_path=details["poster_path"],
            tagline=details["tagline"],
        )

        # get/create genres
        genres = genres_get_or_create(details["genres"])
        movie.save()
        movie.genres.set(genres)
        movie.save()

        if create_collection:
            # create collection unless it exists already
            c = details["belongs_to_collection"]
            if not Collection.objects.filter(id=c["id"]).exists():
                info = tmdb_catch(tmdb.Collections(c["id"]).info)
                if not info:
                    return Response({"error": "Invalid Collection ID"}, status=404)
                collection = Collection(
                    id=info["id"],
                    name=info["name"],
                    overview=info["overview"],
                    poster_path=info["poster_path"],
                    backdrop_path=info["backdrop_path"],
                )
                collection.save()
            else:
                collection = Collection.objects.filter(id=c["id"])[0]

            movie.belongs_to_collection = collection
            movie.save()
    return movie


def set_providers(endpoint,media_object,watch_region:str='DE'):
    providers = tmdb_catch(endpoint,watch_region=watch_region)
    region_providers = providers["results"][watch_region]
    id_list_flatrate = [provider["flatrate"]["provider_id"] for provider in region_providers]
    id_list_buy = [provider["buy"]["provider_id"] for provider in region_providers]
    id_list_rent = [provider["rent"]["provider_id"] for provider in region_providers]
    media_object.providers_flatrate.set(WatchProvider.objects.filter(provider_id__in=id_list_flatrate))
    media_object.providers_buy.set(WatchProvider.objects.filter(provider_id__in=id_list_buy))
    media_object.providers_rent.set(WatchProvider.objects.filter(provider_id__in=id_list_rent))