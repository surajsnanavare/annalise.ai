from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.api.serializers import SignupSerializer


class SignupAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
