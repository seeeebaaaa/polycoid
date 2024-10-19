from rest_framework.decorators import api_view
from rest_framework.response import Response
from time import sleep

@api_view(['POST'])
def button_test_press(request):
    data = request.data
    sleep(3)
    return Response({"message":f"Button was pressed with message: {data.get("message")}"})