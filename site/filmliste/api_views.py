from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from time import sleep
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    ListSerializer,
    DiscoverListsSerializer,
    MovieSerializer,
    TVSeriesSerializer,
    CollectionWithPartsSerializer,
)
from django.shortcuts import redirect
from .models import List, Movie, Genre, Collection, TVSeries, TVSeason, TVEpisode
from django.db.models import Q
from django_hosts.resolvers import reverse
import tmdbsimple as tmdb
from .tmdb_utils import tmdb_catch, genres_get_or_create, movie_get_or_create


@api_view(["POST"])
def button_test_press(request):
    data = request.data
    sleep(3)
    return Response(
        {"message": f"Button was pressed with message: {data.get("message")}"}
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_list(request):
    serializer = ListSerializer(data=request.data)
    if serializer.is_valid():
        list = serializer.save(created_by=request.user)
        return redirect(reverse("index", host="filmliste"))
    return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def discover_lists(request):
    limit_by = 20
    has_more = 0
    query = request.query_params.get("query", "")
    results = List.objects.filter(
        Q(title__icontains=query) | Q(created_by__username__icontains=query)
    )
    if len(results) > limit_by:
        has_more = len(results) - limit_by
    serializer = DiscoverListsSerializer(results[:limit_by], many=True)
    return Response({"results": serializer.data, "has_more": has_more}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_preview(request: Request):
    """This uses the tmdb search/multi and search/collection to list titles to the users"""
    query = request.query_params.get("query", "")
    if not query:
        return Response({"error": "Please provide a query."}, status=400)
    search_obj = tmdb.Search()
    found_media = search_obj.multi(query=query)
    # sort out persons
    found_titles = [
        item for item in found_media["results"] if item.get("media_type") != "person"
    ]
    found_collections = search_obj.collection(query=query)

    return Response(
        {"titles": found_titles, "collections": found_collections}, status=200
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_details_title(request: Request):
    # id of media
    media_id: str = request.query_params.get("id", "")
    if not media_id and not media_id.isdigit():
        return Response({"error": "Bad Media ID"}, status=400)
    media_id: int = int(media_id)

    media_type: str = request.query_params.get("type", "")  # tv, movie
    if not media_type and not (media_type in ["tv", "movie"]):
        return Response({"error": "Bad Media Type"}, status=400)

    # title of the media to check against, in case there is a id<>type miss match
    media_title: str = request.query_params.get("title", "")
    if not media_title:
        return Response({"error": "Bad Media Title"}, status=400)

    # TODO: try/catch for tmdb query if id not exisitng (404 error)
    if media_type == "movie":
        movie = movie_get_or_create(media_id)

        # check if titles match
        if not movie.title == media_title:
            print(movie.title, media_title)
            return Response({"error": "Media<>Title miss match."}, status=400)

        serialized_movie = MovieSerializer(movie)
        return Response(serialized_movie.data, status=200)

        # return the movie data as db object
    elif media_type == "tv":
        # try db first, then tmdb
        tv_series_qs = TVSeries.objects.filter(id=media_id)
        if tv_series_qs.exists():
            # TODO: assuming that if the tv series exists, the seasons and episodes exist too. Should implement a check for that tho at some point.
            tv_series = tv_series_qs[0]  # there can only be one, cause id is pk
        else:
            req_series = tmdb.TV(id=media_id)
            info = tmdb_catch(req_series.info)
            if not info:
                return Response({"error": "Invalid TV ID"}, status=404)

            # create TV series record.
            tv_series = TVSeries(
                id=info["id"],
                backdrop_path=info["backdrop_path"],
                first_air_date=info["first_air_date"],
                last_air_date=info["last_air_date"],
                name=info["name"],
                number_of_seasons=info["number_of_seasons"],
                number_of_episodes=info["number_of_episodes"],
                overview=info["overview"],
                popularity=info["popularity"],
                poster_path=info["poster_path"],
                tagline=info["tagline"],
            )
            tv_series.save()

            # get/create genres
            genres = genres_get_or_create(info["genres"])

            tv_series.genres.set(genres)
            tv_series.save()

            # create all seasons + episodes
            for detail_season in info["seasons"]:
                # get season + episode info
                season_info = tmdb_catch(
                    tmdb.TV_Seasons(
                        tv_id=tv_series.id, season_number=detail_season["season_number"]
                    ).info
                )
                if not season_info:
                    return Response({"error": "Invalid Season ID"}, status=404)

                # create season object
                season = TVSeason(
                    id=season_info["id"],
                    air_date=season_info["air_date"],
                    name=season_info["name"],
                    overview=season_info["overview"],
                    poster_path=season_info["poster_path"],
                    season_number=season_info["season_number"],
                    tv_series=tv_series,
                )
                season.save()
                # create episodes
                for episode_info in season_info["episodes"]:
                    # create episode object
                    episode = TVEpisode(
                        id=episode_info["id"],
                        episode_number=episode_info["episode_number"],
                        name=episode_info["name"],
                        overview=episode_info["overview"],
                        runtime=episode_info["runtime"],
                        season_number=episode_info["season_number"],
                        still_path=episode_info["still_path"],
                        season=season,
                    )
                    episode.save()
        if not tv_series.name == media_title:
            print(tv_series.name, media_title)
            return Response({"error": "Media<>Title miss match."}, status=400)

        serialized_tv_series = TVSeriesSerializer(tv_series)
        return Response(serialized_tv_series.data, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_details_collection(request: Request):
    # id of collection
    collection_id: str = request.query_params.get("id", "")
    if not collection_id and not collection_id.isdigit():
        return Response({"error": "Bad Collection ID"}, status=400)
    collection_id: int = int(collection_id)

    collection_qs = Collection.objects.filter(id=collection_id)
    if collection_qs.exists():
        collection = collection_qs[0]
    else:
        info = tmdb_catch(tmdb.Collections(id=collection_id).info)
        collection = Collection(
            id=info["id"],
            name=info["name"],
            overview=info["overview"],
            poster_path=info["poster_path"],
            backdrop_path=info["backdrop_path"],
        )
        collection.save()
        # create all movies based on parts, if not existend
        for part in info["parts"]:
            if not part["media_type"] == "movie":
                return Response({"error": "TV Collections are not supported."})
            movie = movie_get_or_create(part["id"], create_collection=False)
            movie.belongs_to_collection = collection
            movie.save()

    serialized_collection = CollectionWithPartsSerializer(collection)
    return Response(serialized_collection.data, status=200)
