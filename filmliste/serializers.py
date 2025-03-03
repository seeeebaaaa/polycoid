from rest_framework import serializers
from .models import List, CustomUser


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