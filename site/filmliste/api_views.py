from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from time import sleep
from rest_framework.permissions import IsAuthenticated
from .serializers import ListSerializer, DiscoverListsSerializer
from django.shortcuts import redirect
from .models import List
from django.db.models import Q

@api_view(['POST'])
def button_test_press(request):
    data = request.data
    sleep(3)
    return Response({"message":f"Button was pressed with message: {data.get("message")}"})



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_list(request):
    serializer = ListSerializer(data=request.data)
    if serializer.is_valid():
        list = serializer.save(created_by=request.user)
        return redirect("filmliste:index")
    return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def discover_lists(request):
    limit_by = 20
    has_more = 0
    query = request.query_params.get('query', '')
    results = List.objects.filter(Q(title__icontains=query) | Q(created_by__username__icontains=query))
    if len(results)>limit_by:
        has_more = len(results)-limit_by
    serializer = DiscoverListsSerializer(results[:limit_by], many=True)
    return Response({"results":serializer.data,"has_more":has_more},status=200)