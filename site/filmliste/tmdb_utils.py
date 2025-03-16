from requests.exceptions import HTTPError
from .models import Genre

def tmdb_catch(endpoint):
    """Returns None if 404 or any other error, else just reponse"""
    try:
        result = endpoint()
        return result
    except HTTPError as e:
        return None


def genres_get_or_create(genres_list:list[dict]):
    """Returns Queryset of Genres given. If not already existent, created DB entries for genres."""
    # create genres unless it exists already
    genres = []
    # check if all genres already exist in db
    if not Genre.objects.filter(
        id__in=[g["id"] for g in genres_list]
    ).count() == len(genres_list):
        # if not, create the missing ones
        for genre in genres_list:
            if not Genre.objects.filter(id=genre["id"]).exists():
                new_genre = Genre(id=genre["id"], name=genre["name"])
                new_genre.save()

    # get all gernes objects
    genres = Genre.objects.filter(id__in=[g["id"] for g in genres_list])
    return genres