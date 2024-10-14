from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def button_test_press(request):
    data = request.data
    return Response({"message":f"Button was pressed with message: {data.get("message")}"})