from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from time import sleep
from rest_framework.permissions import IsAuthenticated
from .serializers import ListSerializer
from django.shortcuts import redirect

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