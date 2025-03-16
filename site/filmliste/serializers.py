from rest_framework import serializers
from .models import List, CustomUser, Movie, Collection, Genre, TVSeries, TVSeason, TVEpisode


class ListSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    users = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CustomUser.objects.all(), required=False, default=[]
        )
    

    class Meta:
        model = List
        fields = ['title', 'created_by', 'users', 'colors']
    
    def validate_title(self, value):
        forbidden_words = ["forbidden", "banned"]
        if any(word in value.lower() for word in forbidden_words):
            raise serializers.ValidationError("Title contains forbidden words.")
        return value
    
class DiscoverListsSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['title', 'created_by', 'colors',"id"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name', 'overview', 'poster_path', 'backdrop_path']

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    belongs_to_collection = CollectionSerializer(read_only=True)
    
    class Meta:
        model = Movie
        fields = [
            'id', 
            'title', 
            'overview', 
            'release_date', 
            'runtime', 
            'popularity', 
            'poster_path', 
            'backdrop_path', 
            'tagline',
            'genres',
            'belongs_to_collection'
        ]


class CollectionWithPartsSerializer(serializers.ModelSerializer):
    parts = MovieSerializer(source="movie_set",many=True, read_only=True)
    class Meta:
        model = Collection
        fields = ['id', 'name', 'overview', 'poster_path', 'backdrop_path', 'parts']


class TVEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVEpisode
        fields = [
            'id',
            'episode_number',
            'name',
            'overview',
            'runtime',
            'season_number',
            'still_path'
        ]

class TVSeasonSerializer(serializers.ModelSerializer):
    episodes = TVEpisodeSerializer(many=True, read_only=True)
    episode_count = serializers.SerializerMethodField()
    
    class Meta:
        model = TVSeason
        fields = [
            'id',
            'air_date',
            'name',
            'overview',
            'poster_path',
            'season_number',
            'episodes',
            'episode_count'
        ]
    
    def get_episode_count(self, obj):
        return obj.episodes.count()

class TVSeriesSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    seasons = TVSeasonSerializer(many=True, read_only=True)
    
    class Meta:
        model = TVSeries
        fields = [
            'id',
            'name',
            'overview',
            'first_air_date',
            'last_air_date',
            'popularity',
            'poster_path',
            'backdrop_path',
            'tagline',
            'number_of_seasons',
            'number_of_episodes',
            'genres',
            'seasons'
        ]